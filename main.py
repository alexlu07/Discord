import discord
from discord.ext import commands

with open('.credentials.txt', 'r') as f:
    TOKEN = f.readline().strip()

def cmd(msg, cmd):
    return msg.content.startswith(cmd)

class Cooki(commands.Bot):

    def __init__(self, command_prefix):
        commands.Bot.__init__(self, command_prefix=command_prefix)

        self.channels = dict()
        self.allowed_roles = set()
        self.latest = dict()

        self.register_commands()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    def register_commands(self):
        @self.event
        async def on_message(message):
            if message.channel in self.channels:
                if not message.content == self.channels[message.channel]:
                    await message.delete()
                elif message.author == self.latest[message.channel]:
                    await message.delete()
                else:
                    self.latest[message.channel] = message.author
            else:
                await self.process_commands(message)

        @self.event
        async def on_message_edit(before, after):
            if after.channel in self.channels:
                await after.delete()

        @self.command(aliases=["w"])
        async def watch(ctx, channel):
            if not self.user_perms(ctx.author):
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                self.channels[channel] = "🍪"
                self.latest[channel] = None
                await ctx.message.add_reaction("🍪")
            except Exception as e:

                print(channel)
                msg = await ctx.channel.send("Please enter a valid text channel using #<channel-name>")
                await msg.add_reaction("🍪")

        @self.command(aliases=["uw"])
        async def unwatch(ctx, channel):
            if not self.user_perms(ctx.author):
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                if channel in self.channels:
                    self.channels.pop(channel)
                    self.latest.pop(channel)
                    await ctx.message.add_reaction("🍪")
                else:
                    msg = await ctx.channel.send(f"That channel is not being watched")
                    await msg.add_reaction("🍪")

            except Exception as e:
                print(e)
                msg = await ctx.channel.send("Please enter a valid text channel using #<channel-name>")
                await msg.add_reaction("🍪")

        @self.command(aliases=["wing"])
        async def watching(ctx):
            if not self.user_perms(ctx.author):
                return
            channels_watched = ', '.join([c.mention + 'for ' + self.channels[c] for c in self.channels if c.guild == ctx.guild ])
            msg = await ctx.channel.send(f"Watching channels: {channels_watched if channels_watched else 'None'}")
            await msg.add_reaction("🍪")

        @self.command(aliases=["s"])
        async def set(ctx, channel, *, new_msg):
            if not self.user_perms(ctx.author):
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                if channel in self.channels:
                    self.channels[channel] = new_msg
                    await ctx.message.add_reaction("🍪")
                else:
                    msg = await ctx.channel.send(f"That channel is not being watched")
                    await msg.add_reaction("🍪")

            except Exception as e:
                print(e)
                msg = await ctx.channel.send("Please enter a valid text channel using #<channel-name>")
                await msg.add_reaction("🍪")

    def user_perms(self, user):
        if user.guild_permissions.administrator:
            return True
        if self.allowed_roles.intersection(set(user.roles)):
            return True

        return False


client = Cooki("🍪 ")
client.run(TOKEN)
