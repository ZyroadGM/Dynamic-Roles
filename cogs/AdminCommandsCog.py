# Discord.py Package Import
# ----------------------------
# Json Package Import
import json

from discord.ext import commands


# ----------------------------


class AdminCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["stv", "set-trigger-value"], case_insensitive=True)
    @commands.guild_only()
    async def set_trigger_value(self, ctx, *, trigger_value):
        guild_data = json.load(open("data/guild_data.json"))
        for guild_data_in_list in guild_data['guilds']:
            try:
                guild_data_in_list[str(ctx.guild.id)]['trigger_value'] = trigger_value
                pass
            except:
                continue
        json.dump(guild_data, open("data/guild_data.json", "w"), indent=2)
        await ctx.send(f"Trigger value for \"AutomaticRoles\" is set to `{trigger_value}`!")

    @commands.has_permissions(administrator=True)
    @commands.command(aliases=["set-prefix", "setprefix"], case_insensitive=True)
    @commands.guild_only()
    async def set_prefix(self, ctx, *, prefix):
        guild_data = json.load(open("data/guild_data.json"))
        for guild_data_in_list in guild_data['guilds']:
            try:
                guild_data_in_list[str(ctx.guild.id)]['prefix'] = prefix
                pass
            except:
                continue
        json.dump(guild_data, open("data/guild_data.json", "w"), indent=2)
        await ctx.send(f"Prefix is set to `{prefix}`!")

    @commands.has_permissions(administrator=True)
    @commands.command(case_insensitive=True)
    @commands.guild_only()
    async def on(self, ctx):
        guild_data = json.load(open("data/guild_data.json"))
        for guild_data_in_list in guild_data['guilds']:
            try:
                guild_data_in_list[str(ctx.guild.id)]['AutomaticRoles'] = "ON"
                pass
            except:
                continue
        json.dump(guild_data, open("data/guild_data.json", "w"), indent=2)
        await ctx.send(f"AutomaticRoles is \"ON\"!")

    @commands.has_permissions(administrator=True)
    @commands.command(case_insensitive=True)
    @commands.guild_only()
    async def off(self, ctx):
        guild_data = json.load(open("data/guild_data.json"))
        for guild_data_in_list in guild_data['guilds']:
            try:
                guild_data_in_list[str(ctx.guild.id)]['AutomaticRoles'] = "OFF"
                pass
            except:
                continue
        json.dump(guild_data, open("data/guild_data.json", "w"), indent=2)
        await ctx.send(f"AutomaticRoles is \"OFF\"!")


def setup(client):
    client.add_cog(AdminCommands(client))
    print("AdminCommandsCog.py is loaded!")
