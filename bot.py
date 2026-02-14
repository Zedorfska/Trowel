# bot.py
import os
import discord
from discord.ext import tasks
import random
import json
import re
import requests
import languages
from datetime import date, datetime, timezone, timedelta

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COC_TOKEN = os.getenv("COC_TOKEN")

intents = discord.Intents.all()

class Trowel(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.test")
        await self.load_extension("cogs.clash_of_clans")
        await self.load_extension("cogs.pedro")
        await self.load_extension("cogs.social_credit")
        await self.load_extension("cogs.beton")

bot = Trowel(intents=intents, command_prefix='$')

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
    set_random_status.start()
    #await bot.get_channel(1281595194365710406).send("ubij se")
    #await bot.get_channel(1281590478155943936).send("niti jedan dan da si fulo više...")

@tasks.loop(minutes = 5)
async def set_random_status():
    status_message = "$help"

    quote_list = [
        f"Steam Frame {datetime.now().strftime('%d. %m.')}",            #####
        "Late is just for a little while, suck is forever.",
        "Niko ti meni trebaš.",
        "Ja ne vidim! Ja ne vidim!",
        "Istaknut Povijesničar napada u Clan Waru.",
        "Istaknut Povijesničar odigra svakodašnji Wordle.",
        "Istaknut Povijesničar se obrazuje o riječi dana."
        "Day one no fent.",
        "Needukaciran si.",
        "GABRIJELE, PAZI!",
        "Timeoutam Hrvoja...",
        "Mravionik.",
        "Oh, now there is no sound",
        "Moj dečko ima 8 godin",
        #"Defect from the Guild which has lied to you, Beton member.",
        "Tam sam za 5!",
        "yeah this mf is my GOAT",
        "Is 14 and 17 okay..",
        "Jedan metar bomboclaat UTP kabel",
        "People like... the homosexuals...",
        "AIDA!!!",
        "jel od (((onih)))?",
        "A PET JE POPODNE!!",
        "!! LEAGUE OF LEGENDS DETEKTIRAN !!",
        "Hrvoje....Hrvoje bit ce sve uredu samo te moram izvuc iz Davora....",
        "Zapravo se kaže \"Ni za što\".",
        "Nek se mali najede kurca...",
        "Pa pitaj ChatGPT.",
        ":bliss:",
        "Švarkiram ga.",
        "$pedro",
        "NEVER cutting this shit again",
        "Baba mi je imala moždani udar! 😂😂😂",
        "Bajojajo! Bajojajo!",
        "Jel se tusiras",
        "Juno, okači Zvjezdaninog ćaću na štrik Yandere Sim style.",
        "\"Moram pricat sa Zvjezdanom u vcu cijeli dan💔\"",
        "\"Samoubojstvo *JE* riješenje!\"",
        "Rezanje noktiju nije tako gadno...",
        "Rain BOS",
        "#1 Archivist hater!",
        "❤️ - The one true heart.",
        "♥️ - The root of all evil.",
        "Ne možeš reć'",
        "Zašto si toliko ljut? Nije to tako ozbiljno...",
    ]

    now = datetime.now()

    if now.weekday() == 2:
        quote_list.append(f"Happy {random.choice([ 'Wilson', 'Willow', 'Wolfgang', 'Wendy', 'WX-78', 'Wickerbottom', 'Woodie', 'Wes', 'Maxwell...', 'Wigfrid', 'Webber', 'Winona', 'Warly', 'Wortox', 'Wormwood', 'Wurt', 'Walter', 'Wanda' ])} Wednesday")

    #if now.time() ==

    status_quote = random.choice(quote_list)

    await bot.change_presence(activity=discord.Game(f"{status_message} | {status_quote}"))


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
    await bot.process_commands(message)



async def check_league_of_legends(before, after):
    if not hasattr(after.activity, "name"):
        return
    if hasattr(before.activity, "name"):
        if before.activity.name == "League of Legends":
            return
    if after.activity.name == "League of Legends":
        #add_social_credit(after, -200)
        await bot.get_channel(1281595194365710406).send(f"!!! LEAGUE OF LEGENDS DETEKTIRAN !!!\nKORISNIK: {after.mention} SU UPALILI LEAGUE OF LEGENDS!!!\n~~-200 Social Credit~~")

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
    #await check_mia_clipstudiopaint(before, after)

#
#
#


async def check_democratic_timeout(reaction, user):
    if reaction.message.author.bot:
        return
    if reaction.emoji == "⏰" and reaction.count == 3:
        add_social_credit(reaction.message.author, -200)
        await reaction.message.reply(f"Začepi.\n-200 Social Credit", file = discord.File(r"./Images/Time.png"))
        await reaction.message.author.timeout(datetime.timedelta(minutes = 5), reason = f"Democracy")
        print(f"{reaction.message.author.display_name} timed out democratically")


async def remove_hearts_reaction(reaction, user):
    if reaction.emoji == "♥️":
        gif = discord.File("./videos/Srca.gif")
        await reaction.message.reply("!! inferiorni osjećanik srca detektiran !!", file = gif)
        await reaction.remove(user)

#
# ON REACTION ADD
#

# TODO: make into on_raw_reaction_add
@bot.event
async def on_reaction_add(reaction, user):
    #await remove_hearts_reaction(reaction, user)
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

@bot.command(name = "avatar", help = "Get an avatar from mentioned user")
async def avatar_get(ctx, user: discord.Member = None):
    if user != None:
        await ctx.send(user.avatar)
    else:
        await ctx.send(ctx.author.avatar)

#@bot.command(name = "weather")
#async def weather(ctx):
#    r = requests.get("http://wttr.in/Zagreb?format=j1")
#    weather_json = r.json()
#    print("a")
#    print(weather_json['current_condition']['FeelsLikeC'])
#    await ctx.send(f"Jebote vani je {weather_json['current_condition']['FeelsLikeC']} stupnja celzijevih...")



#       #
# ADMIN #
#       #

def get_language(guild):
    database = load_database()
    return database[str(guild.id)]["config"]["language"]

@bot.command(name = "test", help = "", hidden = True)
async def test(ctx):
    if not is_user_admin(ctx.message.author):
        await ctx.send("Admin command")
        return
    await ctx.send(get_language(ctx.guild))
    await ctx.send(languages.test("test", get_language(ctx.guild)))

@bot.command(name = "test2", help ="", hidden = True)
async def test2(ctx):
    reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    the_channel = bot.get_channel(1373711806257958942)
    await reply.forward(the_channel)


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

@bot.command(name = "listcogs")
async def list_cogs(ctx):
    loaded_cogs = []
    for cog_name in bot.cogs:
        loaded_cogs.append(cog_name)
    await ctx.send(loaded_cogs)

@bot.command(name = "test3")
async def test_3(ctx):
    async for i in ctx.channel.history(limit = 12):
        print(i.author.id)

@bot.command(name = "steam_frame")
async def steam_frame(ctx):
    frame_tomorrow = date.today() + timedelta(days = 1)
    await ctx.send(f"Steam Frame releases {frame_tomorrow.strftime('%d. %m.')}")

bot.run(TOKEN)
