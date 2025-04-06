import logging
import discord
from discord.ext import commands, tasks
from util.log_utils import get_new_events

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_processed_timestamp = None
        self.check_logs.start()

    @tasks.loop(seconds=30)
    async def check_logs(self):
        print("Checking for new server log events")
        new_events, self.last_processed_timestamp = get_new_events(self.last_processed_timestamp)
        if new_events:
            print(f"{len(new_events)} new events found")
            deaths_cog = self.bot.get_cog('Deaths')
            if deaths_cog:
                deaths_cog.process_death_events(new_events)

    @check_logs.before_loop
    async def before_check_logs(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Tasks(bot))