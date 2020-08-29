# Discord.py Package Import
import discord
from discord.ext.commands import Bot
# ----------------------------
# Other Package Imports
import asyncio
import pymongo
import os
from pymongo import MongoClient
from collections import Counter
# ----------------------------
# Random Package Import
import random

# ----------------------------
db = MongoClient("database")


async def determine_prefix(client, message):
    prefix = db.find_one({"_id": str(message.guild.id)})["prefix"]
    if prefix is None:
        db.insert_one({"_id": str(message.guild.id), "prefix": "+", "AutomaticRoles": "OFF", "trigger_value": "2"})
        prefix = "+"
    return prefix


async def determine_trigger_value(client, guild):
    try:
        trigger_value = db.find_one({"_id": str(guild.id)})["trigger_value"]
        return trigger_value
    except:
        db.insert_one({"_id": str(guild.id), "prefix": "+", "AutomaticRoles": "OFF", "trigger_value": "2"})
        return "2"


# Assigns the guild's prefix to bot if command has been run
client = Bot(command_prefix=determine_prefix)


class AutomaticRoles:
    def __init__(self, guild_id):
        self.guild = client.get_guild(guild_id)

    async def get_member_status(self):
        # Resets member data per guild
        member_games_status = []
        members = []
        # ----------------------------
        for member in self.guild.members:
            if member.bot is False:
                game = None
                if member.activities == ():
                    pass
                # Checks if the activity is a game
                elif "' url=" in str(member.activities):
                    game = str(member.activities)[
                           str(member.activities).find("<Activity type=<ActivityType.playing: 0> name='") + len(
                               "<Activity type=<ActivityType.playing: 0> name='"):str(member.activities).rfind("' url=")]
                elif "<Activity type=<ActivityType.playing: 0>" in str(member.activities):
                    # Extracts the game from the data given by member.activities
                    game = str(member.activities)[
                           str(member.activities).find("<Activity type=<ActivityType.playing: 0> name='") + len(
                               "<Activity type=<ActivityType.playing: 0> name='"):str(member.activities).rfind("'")]
                elif "' url=" in str(member.activities):
                    game = str(member.activities)[
                           str(member.activities).find("<Game name='") + len(
                               "<Game name='"):str(member.activities).rfind("' url=")]
                elif "<Game name='" in str(member.activities):
                    game = str(member.activities)[
                           str(member.activities).find("<Game name='") + len(
                               "<Game name='"):str(member.activities).rfind("'")]
                if game is not None:
                    # Appends member data to count and check later
                    members.append(member)
                    member_games_status.append(game)
                    # Adds roles to member by calling function "add_role_to_members"
                    await self.add_role_to_members(game, member)
                else:
                    continue
                await self.process_game(member_games_status, members)

    async def process_game(self, member_games_status, members):
        guild_roles_exists = []
        for game in member_games_status:
            # Checks if the role already exists in the guild and appends them to list
            for guild_role in await self.guild.fetch_roles():
                if guild_role.name == game:
                    guild_roles_exists.append(game)
        # print(list(set(member_games_status) - set(guild_roles_exists)))
        # Counts how many people are playing the same game
        not_existing_roles = list(set(member_games_status) - set(guild_roles_exists))
        games = list(dict.fromkeys(not_existing_roles))
        # Resets member data per guild
        filtered_games_status = []
        filtered_members = []
        # ----------------------------
        for game in games:
            if member_games_status.count(game) >= int(await determine_trigger_value(client, self.guild)):
                # Appends filtered member data to process by role_management() function
                filtered_games_status.append(game)
                for player_game in member_games_status:
                    if player_game == game:
                        filtered_members.append(members[member_games_status.index(player_game)])
        # Adds the member data per member to the role_management() function
        for filtered_game_status in filtered_games_status:
            await self.server_role_management(filtered_game_status)

    async def server_role_management(self, game):
        # Checks if the role already exists in the guild
        guild_role_exists = False
        for guild_role in await self.guild.fetch_roles():
            if guild_role.name == game:
                guild_role_exists = True
        if guild_role_exists is False:
            try:
                await self.guild.create_role(name=game, colour=discord.Color(random.randint(0, 0xffffff)),
                                             mentionable=True,
                                             permissions=discord.Permissions(change_nickname=True, send_messages=True,
                                                                             read_message_history=True, connect=True,
                                                                             speak=True))
                print('-----========-----\n'
                      'Successfully created a role\n'
                      f'{game} in guild {self.guild.id}\n'
                      '-----========-----')
            except:
                pass
        try:
            guild_role_automatic_role = discord.utils.get(self.guild.roles, name="-~~~Automatic Roles~~~-")
            if guild_role_automatic_role is None:
                await self.guild.create_role(name="-~~~Automatic Roles~~~-", colour=discord.Colour.lighter_grey())
            guild_role_ = discord.utils.get(self.guild.roles, name=game)
            await guild_role_.edit(position=guild_role_automatic_role.position - 1)
        except Exception as e:
            print(f"Exception: {e}")

    async def add_role_to_members(self, game, member):
        # Checks if the member already has this role
        member_role_exists = False
        for member_role in member.roles:
            if game == str(member_role):
                member_role_exists = True
        # if member doesn't have the role it adds it
        if member_role_exists is False:
            try:
                await member.add_roles(discord.utils.get(member.guild.roles, name=game))
                print(f"Added {game} role to {member.name} in {self.guild.id}")
            except:
                pass


async def dynamic_roles_active():
    # Runs following code only if the bot is online
    await client.wait_until_ready()
    while not client.is_closed():
        enabled_guilds = []
        # Checks every guild for the status of the attribute 'DynamicRoles'
        for guild_data_in_list in db.find({}):
            # If "DynamicRoles" status is enabled append to "enabled_guilds" list so it could be processed later
            if db.find_one(guild_data_in_list)['AutomaticRoles'] == "ON":
                if client.get_guild(int(db.find_one(guild_data_in_list)["_id"])) is not None:
                    enabled_guilds.append(client.get_guild(int(db.find_one(guild_data_in_list)["_id"])))
            else:
                # If "DynamicRoles" status is disabled take new guild
                continue
        # For guild(s) in "enabled_guilds" run the function DynamicRoles()
        for guild in enabled_guilds:
            try:
                await AutomaticRoles(guild.id).get_member_status()
            except Exception as e:
                print(f"Exception: {e}")

client.loop.create_task(dynamic_roles_active())


async def timer_status():
    await client.wait_until_ready()
    uptime = 0
    while not client.is_closed():
        await asyncio.sleep(60)
        uptime += 1
        await client.change_presence(activity=discord.Activity(status=discord.Status.dnd,
                                                               name=f"for games  [+help] | uptime {uptime}min | servers {db.count_documents({})} | ",
                                                               type=discord.ActivityType.watching))


client.loop.create_task(timer_status())


@client.command(aliases=['trigger-value'], case_insensitive=True)
async def trigger_value(ctx):
    await ctx.send(
        "Your server's trigger value for the \"AutomaticRoles\" is `" + str(
            await determine_trigger_value(client, ctx.guild)) + "`")


if __name__ == "__main__":
    # Removes the default "help"
    client.remove_command("help")
    # Loads all cogs from the cog list
    for cog in ["cogs.StartupCog", "cogs.AdminCommandsCog", "cogs.EventsCog", "cogs.CommandsCog"]:
        try:
            client.load_extension(cog)
        # Print the Exception
        except Exception as e:
            print(f"Exception: {e}")

# Runs the bot with a token found in the "token.txt" file
client.run(open("data/token.txt", "r").read())
