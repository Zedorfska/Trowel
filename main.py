# bot.py
import os
import discord
import datetime
import random
import json

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

# ################## #
# DATABASE FUNCTIONS #
# ################## #

# SAVE AND LOAD
def save_database(data):
    with open("BetonCredit.json", "w") as f:
        json.dump(data, f, indent = 4)

def load_database():
    with open("BetonCredit.json", "r") as f:
        return json.load(f)

# CHECK AND ADD USER
def database_instantiate(user):
    credit_database = load_database()
    if not str(user.id) in credit_database:
        credit_database[user.id] = {
            "name": user.name,
            "credit": 0
        }
        save_database(credit_database)

# SOCIAL CREDIT
def get_social_credit(user):
    database_instantiate(user)
    credit_database = load_database()
    return credit_database[str(user.id)]["credit"]


def add_social_credit(user):
    pass


# ########## #
# BOT EVENTS #
# ########## #

#
@bot.event
async def on_ready():
    print(f'{bot.user}. Up and running.')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "ubi se" in message.content or "ubij se" in message.content or "kys" in message.content:
        await message.channel.send(file=discord.File(r"./Images/KillYourself.jpg"))
    await bot.process_commands(message)

@bot.event
async def on_presence_update(before, after):
    if not hasattr(after.activity, "name"):
        return
    if hasattr(before.activity, "name"):
        if before.activity.name == "League of Legends":
            return
    if after.activity.name == "League of Legends":
        await bot.get_channel(1281595194365710406).send(f"!!! LEAGUE OF LEGENDS DETEKTIRAN !!!\nKORISNIK: {after.mention} JE UPALIO LEAGUE OF LEGENDS!!!")

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == "⏰" and reaction.count == 3:
        await reaction.message.author.timeout(datetime.timedelta(minutes=5), reason=f"Democracy")
        await reaction.message.reply(file=discord.File(r"./Images/Time.png"))
        print(f"{reaction.message.author.id} timed out democratically")


# ############ #
# BOT COMMANDS #
# ############ #

#
@bot.command(name="Setup", help="Set the bot up")
async def setup(ctx):
    #

@bot.command(name="social_standing", help="does the thing")
async def social(ctx):
    social_credit = get_social_credit(ctx.message.author)
    await ctx.send(f"Your social credit score is: " + str(social_credit))


@bot.command(name="stop", help="Stops the bot")
async def stop(ctx):
    if is_user_admin(ctx.message.author):
        exit()
        return
    await ctx.send(f"Fakjumin")

@bot.command(name="ping", help="Pings the bot")
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name="whoami", help="Displays who you are")
async def whoami(ctx):
    is_author_bot_admin : bool = False
    if is_user_admin(ctx.message.author):
        is_author_bot_admin = True
    await ctx.send(f"{ctx.message.author.mention}\nUsername: {ctx.message.author.name}\nDisplay name: {ctx.message.author.display_name}\nTrowel Admin: " + str(is_author_bot_admin))

@bot.command(name="pedro", help="Pedro")
async def pedro(ctx):
    random_pedro = random.randint(0, 39)
    await ctx.channel.send(file=discord.File(r"./Pedro/Pedro" + str(random_pedro) + ".jpg"))

bot.run(TOKEN)
