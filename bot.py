import discord, string, json, os
from discord.ext import commands
from attendance import get_missing_hits
from editfile import get_dict, update_dict, delete_item, list_names
from track import update, topWords, serverTop

intents = discord.Intents.default()
intents.members = True
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
client = commands.Bot(command_prefix='$', intents=intents)
testrole = 870501755987841115
permitted_roles = [741525875572342784, 765081696675823646, 750100932594892917, 742144292193173656, testrole]
dir_path = os.path.dirname(os.path.realpath(__file__))
token = json.load(open(dir_path + "\\config.json"))['token']

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return
    update(message.author.name, string.capwords(message.content))
    await client.process_commands(message)

@client.command(brief='Top words you have spoken!',
                description='Prints the top words that you have spoken',
                aliases=['Top10', 'top10', 'TopWords', 'Topwords', 'topwords'])
async def top_words(ctx):
    await ctx.send('```re\n' + ctx.author.name + '\'s top 10 words:\n' + topWords(ctx.author.name) + '\n```') 

@client.command(brief='Top words everyone has spoken!',
                description='Prints the top words that everyone has spoken',
                aliases=['ServerTop10', 'servertop10', 'ServerTopWords', 'ServerTopwords', 'servertopwords'])
async def server_top_words(ctx):
    await ctx.send('```re\n' + 'Server\'s top 10 words:\n' + serverTop() + '\n```')

@client.command(brief='Annoy someone',
                description='give an ID or a ping, it\'ll quickly ping someone and delete both your message and the ping',
                aliases=['Annoy'])
async def annoy(ctx, id):
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

@client.command(brief='This marks people with the raid role and pings them',
                description='This marks people with the raid role if they have not hit 3 times today, based on the spreadsheet. It then pings raid role in the guild chat.',
                aliases=['Ping'])
async def ping(ctx):
    if not any(role.id in permitted_roles for role in ctx.message.author.roles):
        await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
        return
    spreadsheet_to_discord = get_dict()
    msg = await ctx.send('Pinging')
    members = get_missing_hits()
    #discord_ids takes in everyone who hasn't hit yet (therefore needs a raid role)
    discord_ids = [spreadsheet_to_discord.get(name) for name in members if spreadsheet_to_discord.get(name) != 0]
    role = discord.utils.get(ctx.guild.roles, name="raid")
    for username, discord_id in spreadsheet_to_discord.items():
        person = ctx.guild.get_member(discord_id)
        if person is None or discord_id == 0:
            continue
        if discord_id in discord_ids:
            await person.add_roles(role)
        else:
            await person.remove_roles(role)
    channel = client.get_channel(748969812373274636)
    await msg.delete()
    await channel.send('<@&'+str(869798758462935083)+'> Make sure you do your raids!')
    #await ctx.send('TESTING: Reset in {}!'.format(time_until_reset()))

@client.command(brief='This marks people with the raid role',
                description='This marks people with the raid role if they have not hit 3 times today, based on the spreadsheet.',
                aliases=['Mark'])
async def mark(ctx):
    if not any(role.id in permitted_roles for role in ctx.message.author.roles):
        await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
        return
    spreadsheet_to_discord = get_dict() 
    msg = await ctx.send('Marking...')
    members = get_missing_hits()
    print(members)
    #discord_ids takes in everyone who hasn't hit yet (therefore needs a raid role)
    discord_ids = [spreadsheet_to_discord.get(name) for name in members if spreadsheet_to_discord.get(name) != 0]
    role = discord.utils.get(ctx.guild.roles, name="raid")
    for username, discord_id in spreadsheet_to_discord.items():
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

@client.command(brief='This gets everyone who needs a ping',
                description='This gives a copyable that you can use to ping everyone who hasn\'t hit yet',
                aliases=['getping','Getping','GetPing','get_ping','Get_ping','Get_Ping','getpings','Getpings','GetPings','Get_pings','Get_Pings'])
async def get_pings(ctx):
    if not any(role.id in permitted_roles for role in ctx.message.author.roles):
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

@client.command(brief='This command registers a user in the bot database',
                description='This command registers a user in the bot database so that $mark and $ping works on them',
                aliases=['Register'])
async def register(ctx, spreadsheet_name, discord_id):
    if not any(role.id in permitted_roles for role in ctx.message.author.roles):
        await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
        return
    if not isinstance(spreadsheet_name, str):
        await ctx.send("First argument must be a name!")
    elif not discord_id.isnumeric():
        await ctx.send("Second argument must be a number!")
    else:
        await ctx.send(update_dict(spreadsheet_name[0].capitalize()+spreadsheet_name[1:], discord_id))

@register.error
async def register_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required arguments, use $register <spreadsheet name> <discord id>')

@client.command(brief='This command deletes a user in the bot database',
                description='This command deletes a user in the bot database',
                aliases=['Delete'])
async def delete(ctx, ssname):
    if not any(role.id in permitted_roles for role in ctx.message.author.roles):
        await ctx.send(ctx.message.author.mention + ' You do not have permissions to use this command')
        return
    await ctx.send(delete_item(ssname))

@delete.error
async def delete_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required arguments, use $delete <spreadsheet name>')

@client.command(brief='Lists the users in the database',
                description='This lists all the users currently in the database',
                aliases=['List'])
async def list(ctx):
    await ctx.send('\n'.join(list_names()))
client.run(token)
