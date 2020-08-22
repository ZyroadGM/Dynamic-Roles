# Discord.py Package Import
import discord
from discord.ext import commands
# ----------------------------


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['h', 'cmd', 'commands'], case_insensitive=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="All Commands:",
            colour=discord.Color.dark_blue(),
        )
        embed.set_footer(text=f"")
        embed.add_field(name='----Common Commands----', value="*** ***")
        embed.add_field(name='----Administrator Commands----', value="*** ***")
        embed.add_field(name='wtismysrpx', value="Shows your server's prefix!")
        embed.add_field(name='set_prefix <prefix>{"setprefix", "set-prefix"}', value="You can set your custom prefix for the bot")
        embed.add_field(name='help {"h", "cmd", "commands"}', value="Sends a list of all commands")
        embed.add_field(name='set_trigger_value <trigger_value>{"stv", "set-trigger-value"}', value='You can set your custom trigger value for the "AutomaticRoles"')
        embed.add_field(name='trigger_value {trigger-value}', value="Shows your server's trigger value for the \"AutomaticRoles\"")
        embed.add_field(name='on', value="Turns on automatic roles")
        embed.add_field(name='off', value="Turns off automatic roles")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Commands(client))
    print("CommandsCog.py is loaded!")