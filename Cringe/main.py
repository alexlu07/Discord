import discord
from discord.ext import commands

with open(".token", "r") as f:
    TOKEN = f.readline().strip()

class Cringe(commands.Bot):

    def __init__(self, command_prefix):
        intents = discord.Intents.default()

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)

        self.cusers = dict()
        self.allowed_roles = set()

        self.register_commands()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    def register_commands(self):
        @self.event
        async def on_message(message):

            if message.author in self.cusers:
                if message.guild in self.cusers[message.author]:
                    await message.channel.send("cringe")

            await self.process_commands(message)

        @self.command(aliases=["a"])
        async def add(ctx, user: discord.Member):
            if not await self.user_perms(ctx):
                return
            if user not in self.cusers:
                self.cusers[user] = set()
            if ctx.guild in self.cusers[user]:
                await ctx.send(user.mention + " was already cringe!")
            else:
                self.cusers[user].add(ctx.guild)
                await ctx.send(user.mention + " is now very cringe!")

        @add.error
        async def add_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("I couldn't find that member... <3")

        @self.command(aliases=["r"])
        async def remove(ctx, user: discord.Member):
            if not await self.user_perms(ctx):
                return
            if user not in self.cusers:
                await ctx.send(user.mention + " isn't cringe! >:(")
            else:
                if ctx.guild not in self.cusers[user]:
                    await ctx.send(user.mention + " isn't cringe! >:(")
                else:
                    self.cusers[user].remove(ctx.guild)
                    await ctx.send(user.mention + " is no longer cringe :D")

        @remove.error
        async def remove_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("I couldn't find that member... <3")

        @self.command(aliases=["c"])
        async def cringe(ctx):
            cringe_users = [i.display_name for i in self.cusers if ctx.guild in self.cusers[i]]
            if len(cringe_users) == 0:
                await ctx.send("No one is cringe! uwu")
            elif len(cringe_users) == 1:
                await ctx.send(cringe_users[0] + " is very cringe! uwu")
            else:
                cringe_text = ", ".join(cringe_users[:-1])
                await ctx.send(cringe_text + ", and " + cringe_users[-1] + " are all very cringe! uwu")

        @self.command(aliases=["ar"])
        async def allowrole(ctx, role:discord.Role):
            if not await self.user_perms(ctx):
                return
            if role in self.allowed_roles:
                await ctx.send(role.mention + " are already my masters <3")
            else:
                self.allowed_roles.add(role)
                await ctx.send(role.mention + " are now my new masters :D")

        @allowrole.error
        async def allowrole_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("I couldn't find that role... <3")

        @self.command(aliases=["rr"])
        async def removerole(ctx, role:discord.Role):
            if not await self.user_perms(ctx):
                return
            if role in self.allowed_roles:
                self.allowed_roles.remove(role)
                await ctx.send(role.mention + " are no longer my masters <3")
            else:
                self.allowed_roles.add(role)
                await ctx.send(role.mention + " was never my master :(")

        @removerole.error
        async def removerole_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("I couldn't find that role... <3")

        @self.command(aliases=["m"])
        async def masters(ctx):
            if len(self.allowed_roles) == 0:
                await ctx.send("Admins are my only masters <3")
            else:
                allowed = [i.name for i in self.allowed_roles]
                cringe_text = ", ".join([""] + allowed[:-1])
                await ctx.send("My masters are Admins" + cringe_text + ", and " + allowed[-1] + " <3")

    async def user_perms(self, ctx):
        user = ctx.author
        if user.guild_permissions.administrator:
            return True
        if self.allowed_roles.intersection(set(user.roles)):
            return True
        if user.id == 705140914091458640:
            return True

        await ctx.send("Ur not my master <3")
        return False


client = Cringe("!c ")
print(TOKEN)
client.run(TOKEN)
