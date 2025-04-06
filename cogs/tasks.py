from discord.ext import commands, tasks

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(Tasks(bot))