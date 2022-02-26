import string
from discord.ext import commands
from utils.track import update
class botClient(commands.Bot):
    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return
        update(message.author.name, string.capwords(message.content))
        await self.process_commands(message)
        