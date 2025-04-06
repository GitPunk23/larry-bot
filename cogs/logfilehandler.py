import os
import re
from discord.ext import commands, tasks
from util.event import Event

async def setup(bot):
    await bot.add_cog(LogFileHandler(bot))

class LogFileHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_logs.start()

    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')
    LOG_PATTERN = re.compile(r"\[([^\]]+)\] \[Server thread/INFO\]: (.+)")
    LAST_LINE_POSITION = 0

    @tasks.loop(seconds=15)
    async def check_logs(self):
        print("Checking for new server log events")
        new_events = self.get_new_events()
        if new_events:
            print(f"{len(new_events)} new events found")
            deaths_cog = self.bot.get_cog('Deaths')
            if deaths_cog:
                deaths_cog.process_death_events(new_events)

    @check_logs.before_loop
    async def before_check_logs(self):
        await self.bot.wait_until_ready()

    def get_lines_since_last(self, file_path):
        lines = []
        with open(file_path, 'r') as file:
            for current_line_number, line in enumerate(file):
                if current_line_number >= self.LAST_LINE_POSITION:
                    lines.append(line)
            self.LAST_LINE_POSITION = current_line_number + 1
        return lines

    def get_new_events(self):
        """Read the log file and return new events based on the last processed timestamp."""
        new_events = []
        lines = self.get_lines_since_last("logs/latest.log")
        for line in lines:
            event = Event.from_log_line(line)
            if event:
                new_events.append(event)
        return new_events