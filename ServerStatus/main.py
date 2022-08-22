import discord
from discord.ext import commands, tasks
from mcstatus import JavaServer
import socket

with open(".token", "r") as f:
    TOKEN = f.readline().strip()
    
class ServerStatus(commands.Bot):

    def __init__(self, command_prefix):
        commands.Bot.__init__(self, command_prefix=command_prefix)

        self.watching = dict()
        self.register_commands()

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

        self.update.start()
        

    @tasks.loop(seconds=5)
    async def update(self):
        for key in self.watching:
            _, ip = key
            message = self.watching[key]
            await self.report(message, ip)
            
    async def report(self, message, ip):
        server = JavaServer(ip)
        try:
            status = server.status()
            online = True
            players = status.players.sample if status.players.sample else []
            embed = await self.make_embed(ip, online, [i.name for i in players], status.players.max)
        except (socket.timeout, ConnectionRefusedError):
            online = False
            embed = await self.make_embed(ip, online, [], 0)

        
        await message.edit(content="", embed=embed)

    async def make_embed(self, ip, online, players, max_players):
        color = discord.Color.green() if online else discord.Color.red()
        title = ip
        description = "Status: Online" if online else "Status: Offline"
        
        embed = discord.Embed(color=color, title=title, description=description)

        name = f"Players Online: {len(players)}/{max_players}"
        value = f"Players: [{', '.join(players)}]" if players else "Players: None"
        embed.add_field(name=name, value=value, inline=False)

        return embed

    def register_commands(self):
        @self.command(aliases=["w"])
        async def watch(ctx, channel: discord.TextChannel, ip):
            if (channel, ip) in self.watching:
                await ctx.send("Channel is already watching that ip")
            
            msg = await channel.send("*")
            self.watching[(channel, ip)] = msg

            await self.report(msg, ip)



client = ServerStatus("!ss ")
print(TOKEN)
client.run(TOKEN)

