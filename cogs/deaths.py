from discord.ext import commands
from db import get_discord_id
from util.death_utils import is_death_message

class Deaths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deaths_channel_name = 'deaths' 

    def get_channel_by_name(self, guild, channel_name):
        for channel in guild.channels:
            if channel.name == channel_name:
                return channel
        return None

    def process_death_events(self, events):
        for event in events:
            message = self.get_death_message(event)
            if message:
                guild = self.bot.guilds[0]
                channel = self.get_channel_by_name(guild, self.deaths_channel_name)
                if channel:
                    self.bot.loop.create_task(channel.send(message))

    def get_death_message(self, event):
        if is_death_message(event.event_description):
            discord_id = get_discord_id(event.player)
            if discord_id:
                return f"<@{discord_id}> {event.event_description}"
            else:
                return f"{event.player} {event.event_description}"
        return None

async def setup(bot):
    await bot.add_cog(Deaths(bot))