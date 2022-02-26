import discord, json, os
from botClass import botClient
from botCommands import *
from botCommands.spreadsheet import SpreadSheet

ADMIN_ROLES = [741525875572342784, 765081696675823646, 750100932594892917,
                 742144292193173656, 870501755987841115]

def main():
    token = json.load(open(".\\texts\\config.json"))['token']
    intents = discord.Intents.default()
    intents.members = True

    bot = botClient(
        command_prefix='$',
        help_command = discord.ext.commands.DefaultHelpCommand(
            no_category = 'Commands'
        ),
        intents = intents
    )

    bot.add_cog(topwords.TopWords(bot))
    bot.add_cog(spreadsheet.SpreadSheet(bot, ADMIN_ROLES))
    bot.add_cog(misc.Misc(bot))
    
    bot.run(token)

if __name__ == '__main__':
    main()