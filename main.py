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

        self.register_commands()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    def register_commands(self):
        @self.event())
        async def on_message(message):
            if message.channel in self.channels:
                if not message.content == self.channels[message.channel]:
                    message.delete()
            else:
                await bot.process_commands(message)

        @self.command(aliases=["w"])
        async def watch(ctx, channel):
            if not user_perms(ctx.author):
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                self.channels[channel] = "🍪"
                await ctx.message.add_reaction("🍪")
            except Exception as e:
                print(e)
                msg = await ctx.channel.send("Please enter a valid text channel using #<channel-name>")
                await msg.add_reaction("🍪")

        @self.command(aliases=["uw"])
        async def unwatch(ctx, channel):
            if not user_perms(ctx.author):
                return
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                if channel in self.channels:
                    self.channels.pop(channel)
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
            if not user_perms(ctx.author):
                return
            msg = await ctx.channel.send(f"Watching channels: {', '.join([c.mention + 'for ' + self.channels[c] for c in self.channels]) if self.channels else 'None'}")
            await msg.add_reaction("🍪")

    def user_perms(user):
        if user.guild_permissions.administrator:
            return True
        if self.allowed_roles.intersection(set(user.roles)):
            return True

        return False


client = Cooki("🍪 ")
client.run(TOKEN)
