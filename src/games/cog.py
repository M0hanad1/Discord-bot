from src.games.games import Games
from discord.commands import Option, slash_command
from discord.ext import commands


class GamesCommands(commands.Cog, name='Games'):
    """Games commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.games = Games(self.bot)

    @commands.command(name='random', aliases=['rand'])
    async def command_random(self, ctx):
        """Try to guess the random number"""
        await self.games.random(ctx, False)

    @commands.command(name='fast', aliases=['speed'])
    async def command_fast(self, ctx, lang='random'):
        """Try to type the word as fast as you can"""
        await self.games.typing_games(ctx, lang, 'fast', False)

    @commands.command(name='spell')
    async def command_spell(self, ctx, lang='random'):
        """Try to spell the word as fast as you can"""
        await self.games.typing_games(ctx, lang, 'spell', False)

    @slash_command(name='random')
    async def slash_random(self, ctx):
        """Try to guess the random number"""
        await self.games.random(ctx, True)

    @slash_command(name='fast')
    async def slash_fast(self, ctx, lang: Option(str, 'Language you want to use', choices=['English', 'Arabic', 'Random'], required=False, default='random')):
        """Try to type the word as fast as you can"""
        await self.games.typing_games(ctx, lang, 'fast', True)

    @slash_command(name='spell')
    async def slash_spell(self, ctx, lang: Option(str, 'Language you want to use', choices=['English', 'Arabic', 'Random'], required=False, default='random')):
        """Try to spell the word as fast as you can"""
        await self.games.typing_games(ctx, lang, 'spell', True)


def setup(bot: commands.Bot):
    bot.add_cog(GamesCommands(bot))
