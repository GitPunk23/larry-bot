import discord
from discord.ext import commands
import re
from db import get_minecraft_id 

class Deaths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen for death logs and create a message in the 'deaths' channel."""
        if message.channel.name == 'deaths':  
            death_pattern = re.compile(r"(\w+) \[.*\] (died|was slain)")
            match = death_pattern.search(message.content)
            if match:
                minecraft_id = match.group(1)
                discord_id = get_minecraft_id(minecraft_id)
                
                deaths_channel = discord.utils.get(message.guild.text_channels, name="deaths")
                if deaths_channel:
                    if discord_id:
                        user = await self.bot.fetch_user(discord_id)
                        if user:
                            await deaths_channel.send(f"{user.mention} has died in the game!")
                        else:
                            await deaths_channel.send(f"{minecraft_id} has died in the game!")
                    else:
                        await deaths_channel.send(f"{minecraft_id} has died in the game, but no Discord user is linked.")
                    
def setup(bot):
    bot.add_cog(Deaths(bot))
