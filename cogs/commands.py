import discord
import argparse
from discord.ext import commands
from db import link_user, get_java_id, get_bedrock_id
import shlex

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='link')
    async def link(self, ctx, *, args: str):
        """Link the message sender's Discord user to a Minecraft user."""
        await ctx.message.delete()
        parser = argparse.ArgumentParser()
        parser.add_argument('-j', '--java_id', type=str, help='Java username')
        parser.add_argument('-b', '--bedrock_id', type=str, help='Bedrock username')

        try:
            parsed_args = parser.parse_args(shlex.split(args))
        except SystemExit:
            await ctx.send("Invalid arguments. Use `-j` for Java ID and `-b` for Bedrock ID.")
            return

        discord_id = str(ctx.author.id)
        java_id = parsed_args.java_id
        bedrock_id = parsed_args.bedrock_id

        if java_id:
            if link_user(discord_id, java_id=java_id):
                await ctx.send(f"Successfully linked <@{ctx.author.id}> with Java username {java_id}.")
            else:
                await ctx.send("Failed to link user. Please check the Java username and try again.")
        elif bedrock_id:
            if link_user(discord_id, bedrock_id=bedrock_id):
                await ctx.send(f"Successfully linked <@{ctx.author.id}> with Bedrock username {bedrock_id}.")
            else:
                await ctx.send("Failed to link user. Please check the Bedrock username and try again.")
        else:
            await ctx.send("Please provide either a Java or Bedrock username.")

    @commands.command(name='usernames')
    async def usernames(self, ctx, member: discord.Member = None):
        """Return the saved usernames for the given Discord user."""
        await ctx.message.delete()
        discord_id = str(member.id) if member else str(ctx.author.id)
        java_id = get_java_id(discord_id)
        bedrock_id = get_bedrock_id(discord_id)

        response = f"Usernames for <@{ctx.author.id}>\nJava={java_id}\nBedrock={bedrock_id}"
        await ctx.send(response)

async def setup(bot):
    await bot.add_cog(Commands(bot))