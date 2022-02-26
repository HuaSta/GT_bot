import discord.ext.commands as commands
from utils.track import serverTop, topWords

class TopWords(commands.Cog, name='Top words said'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(brief='Top words you have spoken!',
                    description='Prints the top words that you have spoken',
                    aliases=['Top10', 'top10', 'TopWords', 'Topwords', 'topwords'])
    async def top_words(self, ctx):
        await ctx.send('```re\n' + ctx.author.name + '\'s top 10 words:\n' + topWords(ctx.author.name) + '\n```') 

    @commands.command(brief='Top words everyone has spoken!',
                    description='Prints the top words that everyone has spoken',
                    aliases=['ServerTop10', 'servertop10', 'ServerTopWords', 'ServerTopwords', 'servertopwords'])
    async def server_top_words(self, ctx):
        await ctx.send('```re\n' + 'Server\'s top 10 words:\n' + serverTop() + '\n```')
