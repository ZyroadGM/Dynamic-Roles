# Discord.py Package Import
import discord
from discord.ext import commands
# ----------------------------
# Database Package Import
import pymongo
from pymongo import MongoClient
# ----------------------------
import os

db = MongoClient("database")

class EventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            db.insert_one({"_id": str(guild.id), "prefix": "+", "AutomaticRoles": "OFF", "trigger_value": "2"})
        except:
            print("Already in guild")
        await guild.create_role(name="-~~~Automatic Roles~~~-", colour=discord.Colour.lighter_grey())

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "wtismysrpx":
            prefix = db.find_one({"_id": str(message.guild.id)})["prefix"]
            await message.channel.send(f"Your server's prefix is \"`{prefix}`\"")

    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild):
        db.delete_one({"_id": str(guild.id)})


def setup(client):
    client.add_cog(EventsCog(client))
    print("EventsCog.py is loaded!")
