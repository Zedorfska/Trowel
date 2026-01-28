import discord
import random
import os
from discord.ext import commands

class PedroCog(commands.Cog, name = "Pedro"):
    def __init__(self, bot):
        self.bot = bot

        self.pedro_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pedro"))
        self.images_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Images"))

    @commands.command(name = "pedro", description = "Pedro", help = "Pedro")
    async def pedro(self, ctx):
        files = os.listdir(self.pedro_directory)
        if not files:
            await ctx.send("Something has went terribly wrong and I cannot find the Pedro")
            return
        
        file_name = random.choice(files)
        random_pedro = os.path.join(self.pedro_directory, file_name)

        await ctx.send(file = discord.File(random_pedro))

    @commands.command(name = "peder", hidden = True)
    async def peder(self, ctx):
        file_path = os.path.join(self.images_directory, "peder.jpg")
        await ctx.send(file = discord.File(file_path))

async def setup(bot):
    await bot.add_cog(PedroCog(bot))


