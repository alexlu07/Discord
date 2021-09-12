import discord

with open('credentials.txt', 'r') as f:
    BOT_TOKEN = f.readline().strip()

class Cooki(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if message.content.startswith("-c watch")

client = CustomClient()
client.run(TOKEN)
