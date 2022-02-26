import discord.ext.commands as commands
from utils.track import serverTop, topWords

class Misc(commands.Cog, name='Miscellaneous fun commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Annoy someone',
                description='give an ID or a ping, it\'ll quickly ping someone '
                 + 'and delete both your message and the ping',
                aliases=['Annoy'])
    async def annoy(self, ctx, id):
        if id.isnumeric():
            await ctx.message.delete()
            msg = await ctx.send('<@{}>'.format(id))
            await msg.delete()
        elif '<@' in ctx.message.content:
            await ctx.message.delete()
            msg = await ctx.send(id)
            await msg.delete()
        else:
            await ctx.send('Command failed, try $annoy <ID> or $annoy <ping>')
            print(id)
