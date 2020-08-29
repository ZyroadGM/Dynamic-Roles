# Discord.py Package Imports
import discord
from discord.ext import commands
# ----------------------------
# Database Package Import
import pymongo
from pymongo import MongoClient
# ----------------------------
import os

db = MongoClient("database")


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h', 'cmd', 'commands'], case_insensitive=True)
    async def help(self, ctx):
        prefix = db.find_one({"_id": str(ctx.guild.id)})["prefix"]
        embed = discord.Embed(
            colour=discord.Color.dark_blue(),
        )
        embed.set_footer(text=f"")
        embed.add_field(name='***ℹ️ Information Commands:***', value="*** ***", inline=False)
        embed.add_field(name='`wtismysrpx`', value="Shows your server's prefix!", inline=False)
        embed.add_field(name=prefix + '`help` {"h", "cmd", "commands"}', value="Sends a list of all commands", inline=False)
        embed.add_field(name=prefix + '`trigger_value` {trigger-value}',
                        value="Shows your server's trigger value for the \"AutomaticRoles\"", inline=False)
        embed.add_field(name='***🖥️ Administrator Commands:***', value="*** ***", inline=False)
        embed.add_field(name=prefix + '`set_prefix` <prefix> {"setprefix", "set-prefix"}',
                        value="You can set your custom prefix for the bot", inline=False)
        embed.add_field(name=prefix + '`set_trigger_value` <trigger_value> {"stv", "set-trigger-value"}',
                        value='You can set your custom trigger value for the "AutomaticRoles"', inline=False)
        embed.add_field(name=prefix + '`on`', value="Turns on automatic roles", inline=False)
        embed.add_field(name=prefix + '`off`', value="Turns off automatic roles", inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
    print("CommandsCog.py is loaded!")
