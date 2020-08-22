# Discord.py Package Import
import discord
from discord.ext import commands
# ----------------------------
# Json Package Import
import json
# ----------------------------


class EventsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_data = json.load(open("data/guild_data.json"))
        guild_data['guilds'].append(
        {
            guild.id:
            {
                "prefix": "+",
                "AutomaticRoles": "OFF",
                "trigger_value": "2"
            }
        }
        )
        with open('data/guild_data.json', 'w') as outfile:
            json.dump(guild_data, outfile, indent=2)
        outfile.close()
        await guild.create_role(name="-~~~Automatic Roles~~~-", colour=discord.Colour("#ffffff"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "wtismysrpx":
            guild_data = json.load(open("data/guild_data.json"))
            guild = message.guild
            prefix = None
            for guild_data_in_list in guild_data['guilds']:
                try:
                    # Get the prefix from the guild dict
                    prefix = guild_data_in_list[str(guild.id)]['prefix']
                except:
                    continue
            await message.channel.send(f"Your server's prefix is \"{prefix}\"")


    @commands.Cog.listener()
    async def on_guild_unavailable(self, guild):
        guild_data = json.load(open("data/guild_data.json"))
        for guild_data_in_list in guild_data['guilds']:
            del(guild_data_in_list[str(guild.id)])
        json.dump(guild_data, open("data/guild_data.json", "w"), indent=2)


def setup(client):
    client.add_cog(EventsCog(client))
    print("EventsCog.py is loaded!")

