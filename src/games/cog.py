import discord
from src.games.games import Games
from discord.commands import Option, slash_command
from discord.ext import commands


class GamesCommands(commands.Cog, name='Games'):
    '''Games commands'''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.games = Games(self.bot)

    @commands.command(name='random', aliases=['rand'])
    async def command_random(self, ctx):
        '''Try to guess the random number'''
        await self.games.random(ctx, False)

    @commands.command(name='fast', aliases=['speed'])
    async def command_fast(self, ctx, lang='random'):
        '''Try to type the word as fast as you can'''
        await self.games.typing_games(ctx, lang, 'fast', False)

    @commands.command(name='spell')
    async def command_spell(self, ctx, lang='random'):
        '''Try to spell the word as fast as you can'''
        await self.games.typing_games(ctx, lang, 'spell', False)

    @commands.command(name='roll')
    async def command_roll(self, ctx, min: int=1, max: int=10):
        '''To get a random number with prefix command'''
        await ctx.reply(embed=self.games.roll(ctx, min, max)[0])

    @commands.command(name='8ball')
    async def command_8ball(self, ctx, *, question: str):
        '''To get a random answer for your question'''
        await ctx.reply(embed=self.games.magic_ball(ctx, question))

    @commands.command(name='choose')
    async def command_choose(self, ctx, *, choices: str):
        '''To choose a random choice from your choices'''
        await ctx.reply(embed=self.games.choose(ctx, choices))

    @commands.command(name='tictactoe', aliases=['xo'])
    async def command_tictactoe(self, ctx, member: discord.Member):
        '''To play tictactoe game with other member'''
        temp = await self.games.tictactoe(ctx, member, False)

        if temp:
            await ctx.reply(embed=temp[0])

    @slash_command(name='random')
    async def slash_random(self, ctx):
        '''Try to guess the random number'''
        await self.games.random(ctx, True)

    @slash_command(name='fast')
    async def slash_fast(self, ctx, lang: Option(str, 'Language you want to use', choices=['English', 'Arabic', 'Random'], required=False, default='random')):
        '''Try to type the word as fast as you can'''
        await self.games.typing_games(ctx, lang, 'fast', True)

    @slash_command(name='spell')
    async def slash_spell(self, ctx, lang: Option(str, 'Language you want to use', choices=['English', 'Arabic', 'Random'], required=False, default='random')):
        '''Try to spell the word as fast as you can'''
        await self.games.typing_games(ctx, lang, 'spell', True)

    @slash_command(name='roll')
    async def slash_roll(self, ctx, min: Option(int, 'Min number you want to start with', required=False, default=1), max: Option(int, 'Max number you want to end with', required=False, default=10)):
        '''To get a random number'''
        await ctx.respond(embed=(temp := self.games.roll(ctx, min, max))[0], ephemeral=temp[1])

    @slash_command(name='8ball')
    async def slash_8ball(self, ctx, question: Option(str, 'Question you want to ask')):
        '''To get a random answer for your question'''
        await ctx.respond(embed=self.games.magic_ball(ctx, question))

    @slash_command(name='choose')
    async def slash_choose(self, ctx, choices: Option(str, 'Choices you want to get a random choice from (every choice must end with ",")')):
        '''To choose a random choice from your choices'''
        await ctx.respond(embed=self.games.choose(ctx, choices))

    @slash_command(name='tictactoe')
    async def slash_tictactoe(self, ctx, member: Option(discord.Member, 'Member you want to play with')):
        '''To play tictactoe game with other member'''
        temp = await self.games.tictactoe(ctx, member, True)

        if temp:
            await ctx.respond(embed=temp[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(GamesCommands(bot))
