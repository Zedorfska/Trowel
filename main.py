# bot.py
import os
import discord
import random

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(intents=intents, command_prefix='$')




@bot.event
async def on_ready():
    print(f'{bot.user}. Up and running.')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    #await message.channel.send("Kakav jadan server... Pa ovaj Beton nema ama baš nikakvu povijest...")
    await bot.process_commands(message)



@bot.command(name="ping", help="Pings the bot")
async def ping(ctx):
    await ctx.send("pong")

@bot.command(name="whoami", help="Displays who you are")
async def whoami(ctx):
    print(ctx.message.author.roles)
    AuthorIsAdmin : bool = False
    for i in ctx.message.author.roles:
        print(i)
        if "1426747478560211014" == str(i.id):
            AuthorIsAdmin = True
    await ctx.send(f"Username: {ctx.message.author.name}\nDisplay name: {ctx.message.author.display_name}\nAdmin: " + str(AuthorIsAdmin))

@bot.command(name="pedro", help="Pedro")
async def pedro(ctx):
    RandomPedro = random.randint(0, 9)
    await ctx.channel.send(file=discord.File(r"./Pedro/Pedro" + str(RandomPedro) + ".jpg"))

bot.run(TOKEN)
