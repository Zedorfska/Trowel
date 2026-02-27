from discord.ext import commands, tasks
import requests

class Helldivers2Cog(commands.Cog, name = "Helldivers 2"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hd2_command(self, ctx):
        await ctx.send("Hello from HelldiversCog!")

    @commands.group(invoke_without_command = True, name = "hd2", description = "Helldivers 2")
    async def hd2(self, ctx):
        pass

    @hd2.command(name = "planet", description = "Get info about a specific planet.")
    async def planet(self, ctx, planet_name):
        response = requests.get("https://helldiverstrainingmanual.com/api/v1/planets")
        planets_json = response.json()

        planet_name = planet_name.lower()

        for planet in planets_json.values():
            if planet["name"].lower() == planet_name:
                message = ""

                message += f"# {planet['name']}\n"
                message += f"-# From the **{planet['sector']}** sector\n"

                message += "\n"

                if planet["biome"] != None:
                    message += f"Biome: {planet['biome']['slug']}\n"

                if planet["environmentals"] != []:
                    message += "**Environmentals:**\n"
                    for environmental in planet["environmentals"]:
                        message += f"{environmental['name']}\n"

                await ctx.send(message)
                return

        await ctx.send("No planet of such name. Query is as follows: `$hd2 planet \"Planet Name\"`")

    @hd2.command(name = "major_order", description = "The current major order.")
    async def major_order(self, ctx):
        response = requests.get("https://helldiverstrainingmanual.com/api/v1/war/major-orders")
        major_order_json = response.json()
        
        message = ""
        
        for order in major_order_json:
            message += f"# {order['setting']['overrideTitle']}\n"
            message += f"{order['setting']['overrideBrief']}\n"
            message += f"{order['setting']['taskDescription']}\n"
            message += "\n"

        await ctx.send(message)

    @hd2.command(name = "news")
    async def news(self, ctx, amount = 1):
        response = requests.get("https://helldiverstrainingmanual.com/api/v1/war/news")
        news_json = response.json()

        message = ""

        for new in range(len(news_json)):
            if new < amount:
                message += f"{news_json[new]['message']}\n\n\n"
            else:
                break

        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Helldivers2Cog(bot))


