from discord.ext import commands
import os
import requests
import datetime
from datetime import datetime, timezone
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)
COC_TOKEN = os.getenv("COC_TOKEN")

headers = {
    "Accept": "applications/json",
    "authorization": f"Bearer {COC_TOKEN}"
}

# TODO: automatically send war status announcements

# ts ass
def formatted_war_members(members, state):
    member_with_longest_name = members[0]
    for member in members:
        if len(member["name"]) > len(member_with_longest_name["name"]):
            member_with_longest_name = member
    
    message = ""

    for member in members:
        message += "`"
        message += f"{member['mapPosition']}. "
        if member["mapPosition"] < 10:
            message += " "
        message += f"TH{member['townhallLevel']}"
        if member["townhallLevel"] < 10:
            message += " "
        message += " - "
       
        if state == "inWar":
            for i in range(3):
                if i < member["bestOpponentAttack"]["stars"]:
                    message += "★"
                else:
                    message += "☆"
            message += " "

        message += f"{member['name']}"
    
        for i in range(len(member_with_longest_name["name"]) - len(member['name'])):
            message += " "
        member_attacks = 0
        for attack in member.get("attacks", []):
            member_attacks += 1

        message += f" - {member_attacks}/2"
        message += "`\n"

    return message

class ClashOfClansCog(commands.Cog, name = "Clash of Clans", description = "Perform various CoC related actions"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("a")




    @commands.group(invoke_without_command = True, name = "clan", description = "Clan actions")
    async def clan(self, ctx):
        if ctx.message.content == "$clan":
            await ctx.send(f"This is a command group and requires an argument. Look up `{self.bot.command_prefix}help clan`")
        else:
            await ctx.send(f"Invalid arguments. Try `{self.bot.command_prefix}help clan`")
    


    @clan.command(name = "info", description = "Print clan info")
    async def clan_info(self, ctx):
        response = requests.get("https://cocproxy.royaleapi.dev/v1/clans/%232JJGGJR92", headers = headers)
        info_json = response.json()

        message = ""

        message += f"# {info_json['name']}\n"
        message += f"Level: {info_json['clanLevel']}\n\n"
    
        message += "**Clan members:**\n"

        for member in info_json["memberList"]:
            message += f"{member['name']}\n"

        await ctx.send(message)



    @clan.command(name = "war", description = "Print information about war status")
    async def clan_war(self, ctx):
        response = requests.get("https://cocproxy.royaleapi.dev/v1/clans/%232JJGGJR92/currentwar", headers = headers)
        war_json = response.json()
    
        #TODO: make this a function
        war_start_time_datetime = datetime.strptime(war_json["startTime"], "%Y%m%dT%H%M%S.%fZ")
        war_start_time_epoch = int(war_start_time_datetime.replace(tzinfo=timezone.utc).timestamp())
        war_end_time_datetime = datetime.strptime(war_json["endTime"], "%Y%m%dT%H%M%S.%fZ")
        war_end_time_epoch = int(war_end_time_datetime.replace(tzinfo=timezone.utc).timestamp())
        members = sorted(war_json["clan"]["members"], key = lambda m: m["mapPosition"])
        opponents = sorted(war_json["opponent"]["members"], key = lambda m: m["mapPosition"])
        
        message = ""

        if war_json["state"] == "preparation":
            message += f"# {war_json['clan']['name']} vs {war_json['opponent']['name']}\n"
            message += f"War starts <t:{war_start_time_epoch}:R>\n\n"
        elif war_json["state"] == "inWar":
            message += f"# {war_json['clan']['name']} [ {war_json['clan']['stars']} | {war_json['opponent']['stars']} ] {war_json['opponent']['name']}\n"
            message += f"War ends <t:{war_end_time_epoch}:R>\n\n"
        elif war_json["state"] == "notInWar":
            message += "The times of war lie ahead."
            await ctx.send(message)
            return
        elif war_json["state"] == "warEnded":
            message += "The times of war are long behind us."
            await ctx.send(message)
            return

        message += f"**{war_json['clan']['name']} clan members:**\n"
        message += formatted_war_members(members, war_json["state"])
        message += "\n"
        
        message += f"**{war_json['opponent']['name']} clan members:**\n"
        message += formatted_war_members(opponents, war_json["state"])
        message += "\n"

        await ctx.send(message)

    @clan.command(name = "yell", description = "Yell at people who havent attacked in the war")
    async def clan_yell(self, ctx):
        print("a")

async def setup(bot):
    await bot.add_cog(ClashOfClansCog(bot))


