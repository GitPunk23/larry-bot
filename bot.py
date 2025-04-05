import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import asyncio
import re

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

# Deaths channel name
DEATHS_CHANNEL_NAME = 'deaths'

@bot.event
async def on_ready():
    print(f"Bot is connected as {bot.user}")

async def post_death_to_discord(message):
    """Post the death message to the Discord #deaths channel."""
    for guild in bot.guilds:
        channel = discord.utils.get(guild.text_channels, name=DEATHS_CHANNEL_NAME)
        if channel:
            await channel.send(f"💀 {message}")

bot.run(BOT_TOKEN)
