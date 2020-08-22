# Discord.py Package Import
import discord
from discord.ext.commands import Bot
# ----------------------------
# Other Package Imports
import json
from collections import Counter
# ----------------------------
# Random Package Import
import random
# ----------------------------



async def determine_prefix(client, message):
    guild_data = json.load(open("data/guild_data.json"))
    guild = message.guild
    for guild_data_in_list in guild_data['guilds']:
        try:
            # Get the prefix from the guild dict
            return guild_data_in_list[str(guild.id)]['prefix']
        except:
            continue


async def determine_trigger_value(client, guild):
    guild_data = json.load(open("data/guild_data.json"))
    for guild_data_in_list in guild_data['guilds']:
        try:
            # Get the prefix from the guild dict
            return int(guild_data_in_list[str(guild.id)]['trigger_value'])
        except:
            continue


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
            game = None
            if member.activities == ():
                pass
            # Checks if the activity is a game
            elif "<Activity type=<ActivityType.playing: 0>" in str(member.activities):
                # Extracts the game from the data given by member.activities
                game = str(member.activities)[
                       str(member.activities).find("<Activity type=<ActivityType.playing: 0> name='") + len(
                           "<Activity type=<ActivityType.playing: 0> name='"):str(member.activities).rfind("' ")]
            if "<Game name='" in str(member.activities):
                game = str(member.activities)[
                       str(member.activities).find("<Game name='") + len(
                           "<Game name='"):str(member.activities).rfind("'>")]
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
        count_of_players = dict(Counter(list(set(member_games_status) - set(guild_roles_exists)))).values()
        # Resets member data per guild
        filtered_games_status = []
        filtered_members = []
        # ----------------------------
        filtered_game_count = 0
        for status_count in count_of_players:
            if status_count >= await determine_trigger_value(client, self.guild):
                # Appends filtered member data to process by role_management() function
                filtered_games_status.append(not_existing_roles[filtered_game_count])
                filtered_members.append(members[list(count_of_players).index(status_count)])
            filtered_game_count += 1
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
            except:
                pass


async def dynamic_roles_active():
    # Runs following code only if the bot is online
    await client.wait_until_ready()
    while not client.is_closed():
        enabled_guilds = []
        # Loads guild data from the "guild_data.json" file so it could be used later
        guild_data = json.load(open("data/guild_data.json"))
        for guild in client.guilds:
            # Checks every guild for the status of the attribute 'DynamicRoles'
            for guild_data_in_list in guild_data['guilds']:
                try:
                    # If "DynamicRoles" status is enabled append to "enabled_guilds" list so it could be processed later
                    if guild_data_in_list[str(guild.id)]['AutomaticRoles'] == "ON":
                        enabled_guilds.append(guild)
                except:
                    # If "DynamicRoles" status is disabled take new guild
                    continue
        # For guild(s) in "enabled_guilds" run the function DynamicRoles()
        for guild in enabled_guilds:
            await AutomaticRoles(guild.id).get_member_status()


client.loop.create_task(dynamic_roles_active())

@client.command(aliases=['trigger-value'], case_insensitive=True)
async def trigger_value(ctx):
    await ctx.send(
        f"Your server's trigger value for the \"AutomaticRoles\" is \"{await determine_trigger_value(client, ctx.guild)}\"")


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
