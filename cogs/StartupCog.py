# Discord.py Package Imports
import discord
from discord.ext import commands
# ----------------------------


class Startup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('-----====-----\n'
              'Bot is Online\n'
              f'{self.client.user.name}\n'
              f'-----====-----')
        await self.client.change_presence(
            activity=discord.Activity(status=discord.Status.do_not_disturb, name=f"Bot just started! [+help]", type=discord.ActivityType.watching))


def setup(client):
    client.add_cog(Startup(client))
    print("StartupCog.py is loaded!")
