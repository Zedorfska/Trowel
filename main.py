# bot.py
import os
import discord
import datetime
import random
import json
import re
import requests
import languages
from datetime import datetime, timezone

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COC_TOKEN = os.getenv("COC_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')

headers = {
    "Accept": "application/json",
    "authorization": f"Bearer {COC_TOKEN}"
}



list_of_admins = [
    219526746540736512
    ]

list_of_admin_roles = [
    ]


# ################# #
# GENERAL FUNCTIONS #
# ################# #

# 
def is_user_admin(user):
    if user.id in list_of_admins:
        return True
    else:
        for role in user.roles:
            if role.id in list_of_admin_roles:
                return True
            if role.name == "Trowel Admin":
                return True
    return False

#
#
#

async def get_user(user_id, guild):
    user = guild.get_member(user_id)
    if user == None:
        user = await bot.fetch_user(user_id)
    return user

# TODO: make this work when user not in guild
async def get_user_from_mention(user_mention, guild):
    match = re.match(r"<@!?(?P<id>\d+)>", user_mention)
    if match:
        user_id = int(match.group("id"))
        member = guild.get_member(user_id)
        if member is None:
            try:
                member = await guild.fetch_member(user_id)
            except Exception:
                member = None
        return member

    if user_mention.startswith("@"):
        raw_name = user_mention[1:].strip()

        def normalise(name: str) -> str:
            return re.sub(r"[^a-z0-9]", "", name.lower())

        norm_input = normalise(raw_name)

        for member in guild.members:
            if any(
                norm_input == normalise(value)
                for value in [
                    member.display_name,
                    member.name,
                    getattr(member, "global_name", "") or "",
                ]
            ):
                return member

        for member in guild.members:
            if any(
                norm_input in normalise(value)
                for value in [
                    member.display_name,
                    member.name,
                    getattr(member, "global_name", "") or "",
                ]
            ):
                return member

    return None


# ################## #
# DATABASE FUNCTIONS #
# ################## #

# SAVE AND LOAD
def save_database(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent = 4)

def load_database():
    with open("database.json", "r") as f:
        return json.load(f)

# CHECK AND ADD SERVER
def server_instantiate(server):
    database = load_database()
    if not str(server.id) in database:
        database[server.id] = {
            "config": {
            },
            "social": {
            }
        }
        save_database(database)

# CHECK AND ADD USER
def database_instantiate(user):
    server_instantiate(user.guild)
    database = load_database()
    if not str(user.id) in database[str(user.guild.id)]["social"]:
        database[str(user.guild.id)]["social"][str(user.id)] = {
            "name": user.name,
            "credit": 0
        }
        save_database(database)

# SOCIAL CREDIT
def get_social_credit(user):
    database_instantiate(user)
    database = load_database()
    return database[str(user.guild.id)]["social"][str(user.id)]["credit"]

def add_social_credit(user, amount):
    database_instantiate(user)
    database = load_database()
    database[str(user.guild.id)]["social"][str(user.id)]["credit"] += int(amount)
    save_database(database)
    #return database[str(user.guild.id)]["social"][str(user.id)]["credit"]


#
#
#


async def do_wordle_scoring_against_message(message):
    if not (message.author.id == 1211781489931452447 and " day streak!** 🔥🔥🔥 Here are yesterday's results:" in message.content):
        return

    results = {}

    for line in message.content.splitlines():
        m = re.search(r"(\b\w+/6):\s*(.*)", line)
        if not m:
            continue
        score, users_str = m.groups()

        users = []
        tokens = users_str.split()
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token.startswith("<@"):
                users.append(token)
                i += 1
            elif token.startswith("@"):
                name_tokens = [token]
                i += 1
                while i < len(tokens) and not tokens[i].startswith("<@") and not re.match(r"\w+/6", tokens[i]):
                    name_tokens.append(tokens[i])
                    i += 1
                users.append(" ".join(name_tokens))
            else:
                i += 1
        results[score] = users

    string = "THE RESULTS ARE IN.\n\n"
    for score, user_mentions in results.items():
        for user_mention in user_mentions:
            user = await get_user_from_mention(user_mention, message.guild)
            if user is None:
                string += f"{score} - {user_mention} (User not found)\n"
                continue

            match score:
                case "1/6":
                    string += f"{score} - {user.display_name}. `-800` Social Credit. The state is disappointed.\n"
                    add_social_credit(user, -800)
                case "2/6":
                    string += f"{score} - {user.display_name}. `+500` Social Credit.\n"
                    add_social_credit(user, 500)
                case "3/6":
                    string += f"{score} - {user.display_name}. `+400` Social Credit.\n"
                    add_social_credit(user, 400)
                case "4/6":
                    string += f"{score} - {user.display_name}. `+200` Social Credit.\n"
                    add_social_credit(user, 200)
                case "5/6":
                    string += f"{score} - {user.display_name}. `+100` Social Credit.\n"
                    add_social_credit(user, 100)
                case "6/6":
                    string += f"{score} - {user.display_name}. Inadequate.\n"
                    add_social_credit(user, 0)
                case "X/6":
                    string += f"{score} - {user.display_name}. `-200` Social Credit.\n"
                    add_social_credit(user, -200)

    await message.channel.send(string)


# ########## #
# BOT EVENTS #
# ########## #

# 
# ON READY
#

@bot.event
async def on_ready():
    print(f'{bot.user}. Up and running.')
    await bot.add_cog(Pedro(bot))

#
# ON MESSAGE
#

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        await do_wordle_scoring_against_message(message)
        return
    #if message.author.id == 869617449681682485:
    #    await message.add_reaction("⏰")
    if "ubi se" in message.content.lower() or "ubij se" in message.content.lower() or "kys" in message.content.lower():
        await message.channel.send(file = discord.File(r"./Images/KillYourself.jpg"))
    if "sigm" in message.content.lower():
        await message.channel.send("Ali kada sam ja rekao da sam ja Sigma????")
    if "za ništa" in message.content.lower() or "za nista" in message.content.lower():
        await message.channel.send(f"{message.author}, zapravo se kaže \"[ni za što](https://hjp.znanje.hr/index.php?show=search_by_id&id=eF1uXxA%3D)\".")
    if "ne smije" in message.content.lower():
        await message.channel.send(file = discord.File(r"./Images/NeSmijes.jpg"))
    if "cybersecurity" in message.content.lower() or "sajbersekjuriti" in message.content.lower():
        await message.channel.send(file = discord.File(r"./Videos/Cybersecurity.mp4"))

    await bot.process_commands(message)



async def check_league_of_legends(before, after):
    if not hasattr(after.activity, "name"):
        return
    if hasattr(before.activity, "name"):
        if before.activity.name == "League of Legends":
            return
    if after.activity.name == "League of Legends":
        add_social_credit(after, -200)
        await bot.get_channel(1281595194365710406).send(f"!!! LEAGUE OF LEGENDS DETEKTIRAN !!!\nKORISNIK: {after.mention} SU UPALILI LEAGUE OF LEGENDS!!!\n-200 Social Credit")

async def check_mia_clipstudiopaint(before, after):
    if not after.id == 1123752229552267264:
        return
    if not hasattr(after.activity, "name"):
        return
    if hasattr(before.activity, "name"):
        if before.activity == "CLIP STUDIO PAINT":
            return
    user = await bot.fetch_user("1123752229552267264")
    if not after.activity.name == "CLIP STUDIO PAINT":
        await user.send("Lezbo raspala, pali Clip Studio Paint")
    else:
        await user.send("Fala")

#
# ON PRESENCE UPDATE
#

@bot.event
async def on_presence_update(before, after):
    await check_league_of_legends(before, after)
    await check_mia_clipstudiopaint(before, after)



async def check_democratic_timeout(reaction, user):
    if reaction.message.author.bot:
        return
    if reaction.emoji == "⏰" and reaction.count == 3:
        add_social_credit(reaction.message.author, -200)
        await reaction.message.reply(f"Začepi.\n-200 Social Credit", file = discord.File(r"./Images/Time.png"))
        await reaction.message.author.timeout(datetime.timedelta(minutes = 5), reason = f"Democracy")
        print(f"{reaction.message.author.display_name} timed out democratically")

#
# ON REACTION ADD
#

@bot.event
async def on_reaction_add(reaction, user):
    await check_democratic_timeout(reaction, user)
    # TODO: Starboard


#
# ON
#

@bot.event
async def on_member_join(member):
    await member.guild.system_channel.send(f"{member.mention} su nam se pridružili!")

@bot.event
async def on_member_remove(member):
    await member.guild.system_channel.send(f"{member.mention} su nas napustili!")



# ############ #
# BOT COMMANDS #
# ############ #

#         #
# GENERAL #
#         #

@bot.command(name="serverfetch", help="Linus")
async def serverfetch(ctx):
    embed = discord.Embed(
    title = f"{ctx.guild.name}",
    description = f"Description",
    color = discord.Colour.from_rgb(196, 90, 117))
    embed.set_author(
    name = f"Author Name",
    url = ctx.guild.icon.url,
    icon_url = ctx.guild.icon.url
    )
    embed.set_thumbnail(url = ctx.guild.icon.url)
    embed.add_field(name = f"Kurac", value = f"Palac", inline = False)
    embed.add_field(name = f"Sisa", value = f"Dinamo", inline = True)
    await ctx.send(embed = embed)
    #await ctx.send(f"Server name: {ctx.guild}")

@bot.command(name="whoami", help="Displays who you are")
async def whoami(ctx):
    is_author_bot_admin : bool = False
    if is_user_admin(ctx.message.author):
        is_author_bot_admin = True
    await ctx.send(f"{ctx.message.author.mention}\nUsername: {ctx.message.author.name}\nDisplay name: {ctx.message.author.display_name}\nTrowel Admin: " + str(is_author_bot_admin))


#        #
# SOCIAL #
#        #

@bot.group(name = "social", help = "Perform various social credit actions", invoke_without_command = True)
async def social(ctx):
    if ctx.message.content == "$social":
        await ctx.send(f"This is a command group and requires an argument. Look up `{bot.command_prefix}help social`")
    else:
        await ctx.send(f"Invalid arguments. Try `{bot.command_prefix}help social`")

@social.command(name = "standing")
async def social_standing(ctx):
    social_credit = get_social_credit(ctx.message.author)
    await ctx.send(f"Your social credit score is: {social_credit}")

@social.command(name = "leaderboard", brief = "Highest ranking members by Social Credit", description = "Sends the highest ranking members of the server.")
async def social_leaderboard(ctx, amount = 10):
    database_instantiate(ctx.message.author)
    database = load_database()
    data = database[str(ctx.guild.id)]["social"]
    top = sorted(data.items(), key=lambda x: x[1].get("credit", 0), reverse = True)[:amount]
    string = f"--- TOP {amount} SOCIAL CREDIT HAVERS ---\n\n"
    for i in range(amount):
        if i < len(top):
            string = string + f"{i}. "
            user = await get_user(int(top[i][0]), ctx.guild)
            string = string + f"{user.display_name} - `{top[i][1]['credit']}`\n"
        else:
            break
    await ctx.send(string)

# ADMIN

@social.command(name = "add", hidden = True)
async def social_add(ctx, user: discord.Member = None, amount = None):
    if not is_user_admin(ctx.message.author):
        await ctx.send("erm")
        return
    if user == None or amount == None:
        await ctx.send("Proper format: `social add {user.mention} {amount}`")
        return
    print(user)
    if not isinstance(user, discord.Member):
        await ctx.send("Argument 1 must be a Discord user. `social add {user.mention} {amount}`")
        return
    try:
        amount = int(amount)
    except ValueError:
        await ctx.send("Argument 2 must be int. `social add {user.mention} {amount}`")
        return
    add_social_credit(user, amount)
    await ctx.send(f"Added {amount} social credit to {user.mention}, they now have {get_social_credit(user)} social credit")

#

#       #
# CLASH #
#       #

@bot.group(name = "clan", help = "Perform various CoC clan actions", invoke_without_command = True)
async def clan(ctx):
    if ctx.message.content == "$clan":
        await ctx.send(f"This is a command group and requires an argument. Look up `{bot.command_prefix}help clan`")
    else:
        await ctx.send(f"Invalid arguments. Try `{bot.command_prefix}help clan`")

#

@clan.command(name = "currentwar")
async def clan_currentwar(ctx):
    response = requests.get("https://api.clashofclans.com/v1/clans/%232JJGGJR92/currentwar", headers = headers)
    war_json = response.json()
    start_time = war_json["startTime"]
    start_time_datetime = datetime.strptime(start_time, "%Y%m%dT%H%M%S.%fZ")
    start_time_epoch = int(start_time_datetime.replace(tzinfo=timezone.utc).timestamp())
    members = war_json["clan"]["members"]
    opponents = war_json["opponent"]["members"]
    
    message = ""

    message += f"# {war_json['clan']['name']} vs {war_json['opponent']['name']}\n"
    message += f"CURRENTLY IN {war_json['state'].upper()}\nWar starts <t:{start_time_epoch}:R>\n\n"
    message += f"**Clan members:**\n"
    for member in members:
        message += f"{member['name']}\n"
    message += f"\n"
    message += f"**Opponent clan members:**\n"
    for member in opponents:
        message += f"{member['name']}\n"


    await ctx.send(message)






@bot.command(name = "avatar")
async def avatar_get(ctx, user: discord.Member):
    await ctx.send(user.avatar)

#       #
# PEDRO #
#       #

class Pedro(commands.Cog, name = "Pedro"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "pedro", help = "Pedro")
    async def pedro(self, ctx):
        random_pedro = discord.File(f"./Pedro/{random.choice(os.listdir(R'./Pedro/'))}")
        await ctx.send(file = random_pedro)

    @commands.command(name = "peder", hidden = True)
    async def peder(self, ctx):
        await ctx.send(file = discord.File(f"./Images/peder.jpg"))


#       #
# ADMIN #
#       #

def get_language(guild):
    database = load_database()
    return database[str(guild.id)]["config"]["language"]

@bot.command(name = "test", help = "")
async def test(ctx):
    if not is_user_admin(ctx.message.author):
        await ctx.send("Admin command")
        return
    await ctx.send(get_language(ctx.guild))
    await ctx.send(languages.test("test", get_language(ctx.guild)))


@bot.command(name = "ip", help = "Show the IP this bot is being hosted on")
async def check_ip(ctx):
    r = requests.get("https://ifconfig.me")
    await ctx.send(f"This bot is hosted on `{r.text}`")

@bot.command(name = "stop", help="Stops the bot")
async def stop(ctx):
    if not is_user_admin(ctx.message.author):
        await ctx.send(f"Fakjumin")
        return
    await ctx.send("Doviđenja")
    exit()

@bot.command(name = "ping", help="Pings the bot")
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name = "force_wordle_scoring", hidden = True)
async def test(ctx):
    if not is_user_admin(ctx.message.author):
        await ctx.send("Admin privilidge command")
        return
    reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    await do_wordle_scoring_against_message(reply)

bot.run(TOKEN)
