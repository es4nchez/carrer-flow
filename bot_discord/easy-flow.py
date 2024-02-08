import discord
from discord.ext import commands
import config


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print("Easy-flow bot ready, ready to find some jobs")

bot.load_extension("user_alerting")
bot.load_extension("rappel_cv")
bot.load_extension("send_cv")
bot.load_extension("enterprises_choices")
bot.load_extension("get_tables")
bot.load_extension("import_export")

bot.run(config.DISCORD_BOT_TOKEN)