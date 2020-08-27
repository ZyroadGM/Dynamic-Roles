# Discord.py Package Import
from discord.ext import commands
# ----------------------------
# Json Package Import
import json
import os
# ----------------------------
import pymongo
from pymongo import MongoClient
# ----------------------------
db = MongoClient("database")


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["stv", "set-trigger-value"], case_insensitive=True)
    @commands.guild_only()
    async def set_trigger_value(self, ctx, *, trigger_value):
        if isinstance(int(trigger_value), int) is False:
            await ctx.send("trigger_value is not an integer!")
            return
        db.update_one({"_id": str(ctx.guild.id)}, {"$set": {"trigger_value": trigger_value}})
        await ctx.send(f"Trigger value for \"AutomaticRoles\" is set to `{trigger_value}`!")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["set-prefix", "setprefix"], case_insensitive=True)
    @commands.guild_only()
    async def set_prefix(self, ctx, *, prefix):
        db.update_one({"_id": str(ctx.guild.id)}, {"$set": {"prefix": prefix}})
        await ctx.send(f"Prefix is set to \"`{prefix}`\"!")

    @commands.has_permissions(administrator=True)
    @commands.command(case_insensitive=True)
    @commands.guild_only()
    async def on(self, ctx):
        db.update_one({"_id": str(ctx.guild.id)}, {"$set": {"AutomaticRoles": "ON"}})
        await ctx.send(f"AutomaticRoles is \"ON\"!")

    @commands.has_permissions(administrator=True)
    @commands.command(case_insensitive=True)
    @commands.guild_only()
    async def off(self, ctx):
        db.update_one({"_id": str(ctx.guild.id)}, {"$set": {"AutomaticRoles": "OFF"}})
        await ctx.send(f"AutomaticRoles is \"OFF\"!")


def setup(client):
    client.add_cog(AdminCommands(client))
    print("AdminCommandsCog.py is loaded!")
