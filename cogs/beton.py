import discord
from discord.ext import tasks, commands
from pathlib import Path
from datetime import datetime
import requests
from bs4 import BeautifulSoup

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
IMAGES_DIRECTORY = ROOT_DIRECTORY / "images"
VIDEOS_DIRECTORY = ROOT_DIRECTORY / "videos"

KYS_IMAGE = IMAGES_DIRECTORY / "KillYourself.jpg"
SIGMA_RESPONSE = "Ali kada sam ja rekao da sam ja Sigma????"
NI_ZA_STO_RESPONSE = ", zapravo se kaže \"[ni za što](https://hjp.znanje.hr/index.php?show=search_by_id&id=eF1uXxA%3D)\""
GEORGE_ORWELL_IMAGE = IMAGES_DIRECTORY / "NeSmijes.jpg"
CYBERSECURITY_VIDEO = VIDEOS_DIRECTORY / "Cybersecurity.mp4"

RIJEC_DANA_IMAGE = IMAGES_DIRECTORY / "RijecDanaTrowel.png"

KRIM_TIM_DVA = VIDEOS_DIRECTORY / "15-00.mp4"

# This cog contains random in jokes, you probably want it off
class BetonCog(commands.Cog, name = "Beton"):
    def __init__(self, bot):
        self.bot = bot
        self.krim_tim_dva.start()
    
    @tasks.loop(minutes = 1)
    async def krim_tim_dva(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        #print("Current Time =", current_time)
        if current_time == '15:00':
            channel = self.bot.get_channel(1281595194365710406)
            if channel:
                await channel.send(file=discord.File(KRIM_TIM_DVA))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        kys_triggers = ["ubi se", "ubij se"]
        for trigger in kys_triggers:
            if trigger in message.content.lower():
                await message.channel.send(file = discord.File(KYS_IMAGE))

        sigma_triggers = ["sigma"]
        for trigger in sigma_triggers:
            if trigger in message.content.lower():
                await message.channel.send(SIGMA_RESPONSE)

        ni_za_sto_triggers = ["za nista", "za ništa"]
        for trigger in ni_za_sto_triggers:
            if trigger in message.content.lower():
                await message.channel.send(message.author.name.capitalize() + NI_ZA_STO_RESPONSE)

        george_orwell_triggers = ["ne smije"]
        for trigger in george_orwell_triggers:
            if trigger in message.content.lower():
                await message.channel.send(file = discord.File(GEORGE_ORWELL_IMAGE))

        cybersecurity_triggers = ["cybersecurity", "sajbersekjuriti"]
        for trigger in cybersecurity_triggers:
            if trigger in message.content.lower():
                await message.channel.send(file = discord.File(CYBERSECURITY_VIDEO))

    @commands.command(name = "rijec_dana")
    async def rijec_dana(self, ctx):
        response = requests.get("https://hjp.znanje.hr/word_of_the_day.php")
        content = response.text

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        div = soup.find("div", class_="wd_div")
        word = div.find("b").get_text(strip = True)
        word_type = div.find("i").get_text(strip = True)
        br = div.find("br")
        definition = br.next_sibling.strip()

        more_info_link = div.find_all("a")[-1]["href"]
        response = requests.get(more_info_link)
        soup_more_info = BeautifulSoup(response.text, "html.parser")

        etimologija_div = soup_more_info.find("div", id="etimologija")
        a_tag = etimologija_div.find("a", class_="natlink")
        bold_text = a_tag.find("b").get_text(strip=True)
        prefix_text = etimologija_div.div.contents[0].strip()
        result = f"{prefix_text} {bold_text}"
        etimology = result.lstrip("✧ ").strip()
        
        message = ""
        
        message += f"-# {datetime.today().strftime('%A, %d. %m. %Y.')}\n"

        message += f"# {word}\n"
        message += "\n"
        message += f"-# {word_type}\n"
        message += "\n"
        message += "**Definicija**\n"
        message += f"> {definition}\n"
        message += "\n"
        message += "**Etimologija**\n"
        message += f"> {etimology}\n"
        message += f"-# [Saznaj više...]({more_info_link})\n"
        message += "\n"
        message += "-# *HJPA -* ***#XXX***\n"
        message += "\n"
        message += "-# ||Ovu bezdušnu automatizaciju vam donosi *Trowel*!||\n"
        message += "{ping}"
        
        await ctx.send(file = discord.File(RIJEC_DANA_IMAGE))

        await ctx.send(message)

        


async def setup(bot):
    await bot.add_cog(BetonCog(bot))


