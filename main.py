# bot.py
import os
import discord
import datetime
import random
import json
import re

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')

list_of_admins = [
    219526746540736512
    ]

list_of_admin_roles = [
    "NULL"
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

# TODO: make this work when user not in guild
async def get_user_from_mention(user_mention, guild):
    user_id = user_mention[2:-1]
    user = await guild.fetch_member(user_id)
    return user


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


async def do_wordle_against_message(message):
    if message.author.id == 1211781489931452447 and " day streak!** 🔥🔥🔥 Here are yesterday's results:" in message.content:
        pattern = r"(\b\w+/6):((?: <@[\d]+>)+)"
        matches = re.findall(pattern, message.content)
        results = {}
        for score, users in matches:
            user_list = [u.strip() for u in users.split()]
            results[score] = user_list
        string = "THE RESULTS ARE IN.\n\n"
        for score, users in results.items():
            match score:
                case "1/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. -800 Social Credit. The state is dissapointed.\n"
                        add_social_credit(user, -800)
                case "2/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. +500 Social Credit.\n"
                        add_social_credit(user, 500)
                case "3/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. +400 Social Credit.\n"
                        add_social_credit(user, 400)
                case "4/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. +200 Social Credit.\n"
                        add_social_credit(user, 200)
                case "5/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. +100 Social Credit.\n"
                        add_social_credit(user, 100)
                case "6/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. Inadequate.\n"
                        add_social_credit(user, 0)
                case "X/6":
                    for user_mention in users:
                        user = await get_user_from_mention(user_mention, message.guild)
                        string = string + f"{score} - {user.display_name}. -200 Social Credit.\n"
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

#
# ON MESSAGE
#

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        await do_wordle_against_message(message)
        return
    if "ubi se" in message.content or "ubij se" in message.content or "kys" in message.content:
        await message.channel.send(file=discord.File(r"./Images/KillYourself.jpg"))
    await bot.process_commands(message)



async def check_league_of_legends(before, after):
    if not hasattr(after.activity, "name"):
        return
    if hasattr(before.activity, "name"):
        if before.activity.name == "League of Legends":
            return
    if after.activity.name == "League of Legends":
        add_social_credit(after, -200)
        await bot.get_channel(1281595194365710406).send(f"!!! LEAGUE OF LEGENDS DETEKTIRAN !!!\nKORISNIK: {after.mention} JE UPALIO LEAGUE OF LEGENDS!!!\n-200 Social Credit")

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
    if reaction.emoji == "⏰" and reaction.count == 3:
        add_social_credit(reaction.message.authorl, -200)
        await reaction.message.reply(f"Začepi.\n-200 Social Credit", file=discord.File(r"./Images/Time.png"))
        await reaction.message.author.timeout(datetime.timedelta(minutes=5), reason=f"Democracy")
        print(f"{reaction.message.author.display_name} timed out democratically")

#
# ON REACTION ADD
#

@bot.event
async def on_reaction_add(reaction, user):
    await check_democratic_timeout(reaction, user)


# ############ #
# BOT COMMANDS #
# ############ #


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
    await ctx.send("None or invalid arguments. try `help social`")

@social.command(name = "standing")
async def social_standing(ctx):
    social_credit = get_social_credit(ctx.message.author)
    await ctx.send(f"Your social credit score is: " + str(social_credit))

@social.command(name = "leaderboard")
async def social_leaderboard(ctx, amount = 10):
    database = load_database()
    data = database[str(ctx.guild.id)]["social"]
    top = sorted(data.items(), key=lambda x: x[1].get("credit", 0), reverse=True)[:amount]
    string = f"--- TOP {amount} SOCIAL CREDIT HAVERS ---\n\n"
    for i in range(amount):
        if i < len(top):
            # TODO: only perform this check if necesarry
            user = await bot.fetch_user(top[i][0])
            string = string + f"{user.display_name} - {top[i][1]['credit']}\n"
        else:
            break
    await ctx.send(string)

@social.command(name = "add")
async def social_add(ctx, user: discord.Member = None, amount = None):
    if not is_user_admin(ctx.message.author):
        await ctx.send("erm")
        return
    if user == None or amount == None:
        await ctx.send("Proper format: `social add {user.mention} {amount}`")
        return
    if not isinstance(user, discord.Member):
        await ctx.send("Argument 1 must be a Discord user. `social add {user.mention} {amount}`")
        return
    if amount.isdigit():
        amount = int(amount)
    else:
        await ctx.send("Argument 2 must be int. `social add {user.mention} {amount}`")
        return
    add_social_credit(user, amount)
    await ctx.send(f"Added {amount} social credit to {user.mention}, they now have {get_social_credit(user)} social credit")

#       #
# PEDRO #
#       #

@bot.command(name="pedro", help="Pedro")
async def pedro(ctx):
    random_pedro = random.randint(0, 39)
    await ctx.channel.send(file=discord.File(r"./Pedro/Pedro" + str(random_pedro) + ".jpg"))

#       #
# DEBUG #
#       #

@bot.command(name="stop", help="Stops the bot")
async def stop(ctx):
    if not is_user_admin(ctx.message.author):
        await ctx.send(f"Fakjumin")
        return
    exit()

@bot.command(name="ping", help="Pings the bot")
async def ping(ctx):
    await ctx.send("pong")

#      #
# TEST #
#      #

@bot.command(name="force_wordle_scoring")
async def test(ctx):
    if not is_user_admin(ctx.message.author):
        ctx.send("Admin privilidge command")
        return
    reply = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    await do_wordle_against_message(reply)

bot.run(TOKEN)
