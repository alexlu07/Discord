import discord
from discord.ext import commands

with open('.credentials.txt', 'r') as f:
    TOKEN = f.readline().strip()

def cmd(msg, cmd):
    return msg.content.startswith(cmd)

class Cooki(commands.Bot):

    def __init__(self, command_prefix):
        commands.Bot.__init__(self, command_prefix=command_prefix)

        self.channels = set()

        self.register_commands()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    def register_commands(self):
        @self.command(aliases=["w"])
        async def watch(ctx, channel):
            try:
                channel = await commands.TextChannelConverter().convert(ctx, channel)
                self.channels.add(channel)
                await ctx.message.add_reaction("🍪")
            except Exception as e:
                print(e)
                msg = await ctx.channel.send("Please enter a valid text channel using #<channel-name>")
                await msg.add_reaction("🍪")

        # @self.command(aliasess=["wing"])


    # async def on_message(self, message):
    #     if cmd(message, "🍪 watch") or cmd(message, "🍪 w"):
    #         if cmd(message, "🍪 watching") or cmd(message, "🍪 wing"):
    #             msg = await message.channel.send(f"Watching channels: {', '.join([c.mention for c in self.channels])}")
    #             await msg.add_reaction("🍪")

    #         else:
    #             for c in message.channel_mentions:
    #                 if type(c) == discord.TextChannel:
    #                     self.channels.add(c)
    #                     await message.add_reaction("🍪")
    #                     break
    #             else:
    #                 msg = await message.channel.send("Please enter a valid text channel using #<channel-name>")
    #                 await msg.add_reaction("🍪")


client = Cooki("🍪 ")
client.run(TOKEN)
