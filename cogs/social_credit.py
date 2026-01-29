from discord.ext import commands

class SocialCreditCog(commands.Cog, name = "Social Credit"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def social_command(self, ctx):
        await ctx.send("Social credit!")

async def setup(bot):
    await bot.add_cog(SocialCreditCog(bot))


