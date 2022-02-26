import discord
import discord.ext.commands as commands
from attendance import get_missing_hits
from utils.editfile import get_dict, update_dict, delete_item, list_names

class SpreadSheet(commands.Cog, name='Spreadsheet-to-discord bridge'):

    def __init__(self, bot, permitted_roles):
        self.bot = bot
        self.permitted_roles = permitted_roles

    @commands.command(brief='This marks people with the raid role and pings them',
                    description='This marks people with the raid role if they have not hit 3 times today, '
                            + 'based on the spreadsheet. It then pings raid role in the guild chat.',
                    aliases=['Ping'])
    async def ping(self, ctx):
        if not any(role.id in self.permitted_roles for role in ctx.message.author.roles):
            await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
            return
        spreadsheet_to_discord = get_dict()
        msg = await ctx.send('Pinging')
        members = get_missing_hits()
        #discord_ids takes in everyone who hasn't hit yet (therefore needs a raid role)
        discord_ids = [spreadsheet_to_discord.get(name) for name in members if spreadsheet_to_discord.get(name) != 0]
        role = discord.utils.get(ctx.guild.roles, name="raid")
        for _, discord_id in spreadsheet_to_discord.items():
            person = ctx.guild.get_member(discord_id)
            if person is None or discord_id == 0:
                continue
            if discord_id in discord_ids:
                await person.add_roles(role)
            else:
                await person.remove_roles(role)
        channel = self.bot.get_channel(748969812373274636)
        await msg.delete()
        await channel.send('<@&'+str(869798758462935083)+'> Make sure you do your raids!')

    @commands.command(brief='This marks people with the raid role',
                    description='This marks people with the raid role if they have not hit '
                     + '3 times today, based on the spreadsheet.',
                    aliases=['Mark'])
    async def mark(self, ctx):
        if not any(role.id in self.permitted_roles for role in ctx.message.author.roles):
            await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
            return
        spreadsheet_to_discord = get_dict() 
        msg = await ctx.send('Marking...')
        members = get_missing_hits()
        print(members)
        #discord_ids takes in everyone who hasn't hit yet (therefore needs a raid role)
        discord_ids = [spreadsheet_to_discord.get(name) for name in members if spreadsheet_to_discord.get(name) != 0]
        role = discord.utils.get(ctx.guild.roles, name="raid")
        for _, discord_id in spreadsheet_to_discord.items():
            person = ctx.guild.get_member(discord_id)
            if person is None or discord_id == 0:
                continue
            if discord_id in discord_ids:
                await person.add_roles(role)
            else:
                await person.remove_roles(role)
        discord_ids = ['<\@' + str(discord_id) + '>' for discord_id in discord_ids] 
        await msg.delete()
        await ctx.send('marked ' + ', '.join(members))
        await ctx.send('copyable: ' + ' '.join(discord_ids))

    @commands.command(brief='This gets everyone who needs a ping',
                    description='This gives a copyable that you can use to ping everyone who hasn\'t hit yet',
                    aliases=['getping','Getping','GetPing','get_ping','Get_ping','Get_Ping',
                            'getpings','Getpings','GetPings','Get_pings','Get_Pings'])
    async def get_pings(self, ctx):
        if not any(role.id in self.permitted_roles for role in ctx.message.author.roles):
            await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
            return
        spreadsheet_to_discord = get_dict()
        msg = await ctx.send('Getting pings...')
        members = get_missing_hits()
        discord_ids = [spreadsheet_to_discord.get(name) for name in members if spreadsheet_to_discord.get(name) != 0]
        discord_ids = ['<\@' + str(discord_id) + '>' for discord_id in discord_ids] 
        await msg.delete()
        await ctx.send('Got pings of: ' + ', '.join(members))
        await ctx.send('copyable: ' + ' '.join(discord_ids))

    @commands.command(brief='This command registers a user in the bot database',
                    description='This command registers a user in the bot database so that $mark and $ping works on them',
                    aliases=['Register'])
    async def register(self, ctx, spreadsheet_name, discord_id):
        if not any(role.id in self.permitted_roles for role in ctx.message.author.roles):
            await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
            return
        if not isinstance(spreadsheet_name, str):
            await ctx.send("First argument must be a name!")
        elif not discord_id.isnumeric():
            await ctx.send("Second argument must be a number!")
        else:
            await ctx.send(update_dict(spreadsheet_name[0].capitalize()+spreadsheet_name[1:], discord_id))

    @register.error
    async def register_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required arguments, use $register <spreadsheet name> <discord id>')

    @commands.command(brief='This command deletes a user in the bot database',
                    description='This command deletes a user in the bot database',
                    aliases=['Delete'])
    async def delete(self, ctx, ssname):
        if not any(role.id in self.permitted_roles for role in ctx.message.author.roles):
            await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
            return
        await ctx.send(delete_item(ssname))

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Missing required arguments, use $delete <spreadsheet name>')

    @commands.command(brief='Lists the users in the database',
                    description='This lists all the users currently in the database',
                    aliases=['List'])
    async def list(self, ctx):
        await ctx.send('\n'.join(list_names()))
