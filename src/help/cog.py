import discord
from discord.ext import commands
from discord.commands import slash_command
from src.help.help import Help


class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.help = Help(bot)

    @commands.command(name='help')
    async def command_help(self, ctx):
        await self.help.send_bot_help(ctx, False, self.bot.cogs)

    @slash_command(name='help', guild_ids=[934444583998353489])
    async def slash_help(self, ctx):
        '''Send bot help command'''
        await self.help.send_bot_help(ctx, True, self.bot.cogs)


def setup(bot: commands.Bot):
    bot.add_cog(HelpCommand(bot))
