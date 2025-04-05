import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
MINECRAFT_LOG_PATH = '/path/to/your/minecraft/server/logs/latest.log'  # Update this path

# Set up intents
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

# Initialize the bot
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f"Bot is connected as {bot.user}")

bot.run(BOT_TOKEN)
