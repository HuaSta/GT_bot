import discord, sys, traceback, asyncio
from discord.ext import commands


class CommandErrHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandNotFound):
            msg = await ctx.send('Command not found')
            await asyncio.sleep(3)
            await msg.delete()
        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            msg = await ctx.send('Command {} has errored! Check your inputs'.format(ctx.command))
            await asyncio.sleep(3)
            await msg.delete()