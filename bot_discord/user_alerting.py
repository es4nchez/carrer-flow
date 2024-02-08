import discord
from discord.ext import commands, tasks
import datetime
from datetime import datetime, timedelta
import logging


LOG = logging

class UserAlerting(commands.Cog):
    def __init__(self, bot):
        LOG.info(f"Initialized {self.__class__.__name__}")
        self.bot = bot
       # self.time_alerts = {"days": [1], "hours": [1], "minutes": [15, 1]}  # Hardcoded time for alerting, tbd if permanent / editable
        self.time_alerts = {"minutes": [15, 1]} # Demo purpose
        rdv1 =    datetime.now() + timedelta(minutes=5)  # Hardcoded at start for demo
        rdv2 =    datetime.now() + timedelta(minutes=17) # Hardcoded at start for demo
        rdv3 =    datetime.now() + timedelta(minutes=18) # Hardcoded at start for demo
        self.alerts_db = {  # Hardcoded, to be linked with the database of interviews, and to the intra / discord user
            "es4nchez": [
                {"company": "Groupe mutuel", "name_of_post": "Software Developer", "hour_of_interview": f"{rdv1}", "Room": "SSD", "alerts_sent": []},
                {"company": "Infomaniak", "name_of_post": "Data Analyst", "hour_of_interview": f"{rdv2}", "Room": "Asgard", "alerts_sent": []}
            ],
            "__vincent": [
                {"company": "42 Lausanne", "name_of_post": "Rust Senior Dev", "hour_of_interview": f"{rdv3}", "Room": "Upside Down", "alerts_sent": []}
            ]
        }


    @tasks.loop(seconds=10.0)
    async def alert_users(self):
        now = datetime.now()
        for user_name, interviews in list(self.alerts_db.items()):
            user_discord = discord.utils.get(self.bot.guilds[0].members, name=user_name) # Maybe a more efficient way
            if not user_discord:
                continue
            for interview in interviews[:]:
                interview_time = datetime.strptime(interview['hour_of_interview'], "%Y-%m-%d %H:%M:%S.%f")

                for time_unit, deltas in self.time_alerts.items():
                    for delta in deltas:
                        alert_key = f"{delta}_{time_unit}_alert_sent"
                        alert_time = interview_time - timedelta(**{time_unit: delta})

                        if alert_time <= now < interview_time and alert_key not in interview["alerts_sent"]:
                            reminder_title = f"\U000023F0 Reminder: Your interview is in {delta} {time_unit}!"
                            await self.send_reminder(user_discord, user_name, interview, reminder_title)
                            interview["alerts_sent"].append(alert_key)

                if now >= interview_time:
                    interviews.remove(interview)

            if not interviews:
                del self.alerts_db[user_name]


    async def send_reminder(self, user_discord, user_name, interview, title):
        interview_time = datetime.strptime(interview['hour_of_interview'], "%Y-%m-%d %H:%M:%S.%f")
        timestamp = int(interview_time.timestamp())
        embed = discord.Embed(title=title, color=0x00ff00)
        embed.add_field(name=":bust_in_silhouette: Login:", value=user_name, inline=False)
        embed.add_field(name=":briefcase: Company:", value=interview['company'], inline=True)
        embed.add_field(name=":computer: Position:", value=interview['name_of_post'], inline=True)
        embed.add_field(name=":timer: Time", value=f"<t:{timestamp}:f>", inline=False)
        embed.add_field(name=":round_pushpin: Room:", value=interview['Room'], inline=True)
        await user_discord.send(embed=embed)


    @commands.Cog.listener()
    async def on_ready(self):
        self.alert_users.start()


def setup(bot):
    bot.add_cog(UserAlerting(bot))