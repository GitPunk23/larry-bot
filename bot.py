import logging
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
from db import init_db  # Import the init_db function

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is connected as {bot.user}")

async def load_extensions():
    await bot.load_extension('cogs.deaths')
    await bot.load_extension('cogs.tasks')
    await bot.load_extension('cogs.commands')

async def main():
    init_db()
    async with bot:
        await load_extensions()
        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())