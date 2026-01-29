import discord
from discord.ext import commands
from pathlib import Path

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
IMAGES_DIRECTORY = ROOT_DIRECTORY / "images"
VIDEOS_DIRECTORY = ROOT_DIRECTORY / "videos"

KYS_IMAGE = IMAGES_DIRECTORY / "KillYourself.jpg"
SIGMA_RESPONSE = "Ali kada sam ja rekao da sam ja Sigma????"
NI_ZA_STO_RESPONSE = ", zapravo se kaže \"[ni za što](https://hjp.znanje.hr/index.php?show=search_by_id&id=eF1uXxA%3D)\""
GEORGE_ORWELL_IMAGE = IMAGES_DIRECTORY / "NeSmijes.jpg"
CYBERSECURITY_VIDEO = VIDEOS_DIRECTORY / "Cybersecurity.mp4"


# This cog contains random in jokes, you probably want it off
class BetonCog(commands.Cog, name = "Beton"):
    def __init__(self, bot):
        self.bot = bot

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

async def setup(bot):
    await bot.add_cog(BetonCog(bot))


