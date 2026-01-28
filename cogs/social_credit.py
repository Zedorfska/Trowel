from discord.ext import commands

class TestCog(commands.Cog, name = "Test Cog"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def super_command(self, ctx):
        await ctx.send("Hello from SuperCog!")

async def setup(bot):
    await bot.add_cog(TestCog(bot))


