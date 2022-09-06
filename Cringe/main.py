import discord
from discord.ext import commands

with open(".token", "r") as f:
    TOKEN = f.readline().strip()

class Cringe(commands.Bot):

    def __init__(self, command_prefix):
        intents = discord.Intents.default()
        intents.message_content = True

        commands.Bot.__init__(self, command_prefix=command_prefix, intents=intents)

        self.cusers = dict()
        self.allowed_roles = set()
        self.allowed_users = set()

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
                await ctx.send(user.mention + " was already cringe")
            else:
                self.cusers[user].add(ctx.guild)
                await ctx.send(user.mention + " is now extremely cringe")

        @add.error
        async def add_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("who is that")

        @self.command(aliases=["r"])
        async def remove(ctx, user: discord.Member):
            if not await self.user_perms(ctx):
                return
            if user not in self.cusers:
                await ctx.send(user.mention + " wasn't on my list")
            else:
                if ctx.guild not in self.cusers[user]:
                    await ctx.send(user.mention + " wasn't on my list")
                else:
                    self.cusers[user].remove(ctx.guild)
                    await ctx.send(user.mention + " is no longer cringe")

        @remove.error
        async def remove_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("who is that")

        @self.command(aliases=["c"])
        async def cringe(ctx):
            cringe_users = [i.display_name for i in self.cusers if ctx.guild in self.cusers[i]]
            if len(cringe_users) == 0:
                await ctx.send("No one is cringe (for now)")
            elif len(cringe_users) == 1:
                await ctx.send(cringe_users[0] + " is very cringe")
            else:
                cringe_text = ", ".join(cringe_users[:-1])
                await ctx.send(cringe_text + ", and " + cringe_users[-1] + " are all extremely cringe")

        @self.command(aliases=["ar"])
        async def allowrole(ctx, role:discord.Role):
            if not await self.user_perms(ctx):
                return
            if role in self.allowed_roles:
                await ctx.send(role.mention + " already have permissions")
            else:
                self.allowed_roles.add(role)
                await ctx.send(role.mention + " have now been given permissions")

        @allowrole.error
        async def allowrole_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("Role does not exist")

        @self.command(aliases=["rr"])
        async def removerole(ctx, role:discord.Role):
            if not await self.user_perms(ctx):
                return
            if role in self.allowed_roles:
                self.allowed_roles.remove(role)
                await ctx.send(role.mention + " no longer have permissions")
            else:
                await ctx.send(role.mention + " didn't have permissions in the first place")

        @removerole.error
        async def removerole_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("Role does not exist")

        @self.command(aliases=["au"])
        async def allowuser(ctx, user: discord.Member):
            if not await self.user_perms(ctx):
                return
            if user in self.allowed_users:
                await ctx.send(user.mention + " already has permissions")
            else:
                self.allowed_users.add(user)
                await ctx.send(user.mention + " has now been given permissions")
        
        @allowuser.error
        async def allowuser_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("who is that")

        @self.command(aliases=["ru"])
        async def removeuser(ctx, user: discord.Member):
            if not await self.user_perms(ctx):
                return
            if user in self.allowed_users:
                self.allowed_users.remove(user)
                await ctx.send(user.mention + " no longer has permissions")
            else:
                await ctx.send(user.mention + " didn't have permissions in the first place")
        
        @removeuser.error
        async def removeuser_error(ctx, error):
            if not await self.user_perms(ctx):
                return
            if isinstance(error, commands.BadArgument):
                await ctx.send("who is that")

        @self.command(aliases=["p"])
        async def perms(ctx):
            if len(self.allowed_roles) == 0:
                await ctx.send("Only admins have permission")
            else:
                allowed = [i.name for i in self.allowed_roles]
                cringe_text = ", ".join([""] + allowed[:-1])
                await ctx.send("Admins" + cringe_text + ", and " + allowed[-1] + " have permissions")

    async def user_perms(self, ctx):
        user = ctx.author
        if user.guild_permissions.administrator:
            return True
        if self.allowed_roles.intersection(set(user.roles)):
            return True
        if user in self.allowed_users:
            return True
        if user.id == 705140914091458640:
            return True

        await ctx.send("U don't have permission L")
        return False


client = Cringe("!c ")
print(TOKEN)
client.run(TOKEN)
