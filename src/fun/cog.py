import discord
from src.fun.games import Fun
from discord.commands import Option, slash_command
from discord.ext import commands
from src.functions.functions import create_embeds


class FunCommands(commands.Cog, name='Fun'):
    '''Fun commands'''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.fun = Fun(self.bot)

    @commands.command(name='random', aliases=['rand'], description='Try to guess the random number')
    async def command_random(self, ctx):
        '''{prefix}random'''
        await self.fun.random(ctx, False)

    @commands.command(name='fast', aliases=['speed'], description='Try to type the word as fast as you can')
    async def command_fast(self, ctx, language='random'):
        '''{prefix}fast
        {prefix}fast arabic
        {prefix}fast english
        '''
        await self.fun.typing_games(ctx, language, 'fast', False)

    @commands.command(name='spell', description='Try to spell the word as fast as you can')
    async def command_spell(self, ctx, language='random'):
        '''{prefix}spell
        {prefix}spell ar
        {prefix}spell en
        '''
        await self.fun.typing_games(ctx, language, 'spell', False)

    @commands.command(name='say', description='Make the bot say something')
    async def command_say(self, ctx, *, message):
        '''{prefix}say Hello There
        {prefix}say Hello {mention}
        '''
        await ctx.reply(embed=create_embeds(ctx, ('', message)))

    @commands.command(name='roll', description='Get a random number with prefix command')
    async def command_roll(self, ctx, min: int=1, max: int=10):
        '''{prefix}roll
        {prefix}roll 2
        {prefix}roll 10 15
        '''
        await ctx.reply(embed=self.fun.roll(ctx, min, max)[0])

    @commands.command(name='8ball', description='Get a random answer for your question')
    async def command_8ball(self, ctx, *, question: str):
        '''{prefix}8ball I'm gonna work with google?'''
        await ctx.reply(embed=self.fun.magic_ball(ctx, question))

    @commands.command(name='choose', description='Choose a random choice')
    async def command_choose(self, ctx, *, choices: str):
        '''{prefix}choose Python, C#, C++, TypeScript'''
        await ctx.reply(embed=self.fun.choose(ctx, choices))

    @commands.command(name='tictactoe', aliases=['xo'], description='Play tictactoe game with other member')
    async def command_tictactoe(self, ctx, member: discord.Member):
        '''{prefix}tictactoe {mention}'''
        temp = await self.fun.tictactoe(ctx, member, False)

        if temp:
            await ctx.reply(embed=temp[0])

    @commands.command(name='roshambo', description='Play roshambo(Rock-Paper-Scissors) game with [me, member]')
    async def command_roshambo(self, ctx, member: discord.Member=None):
        '''{prefix}roshambo
        {prefix}roshambo {mention}
        '''
        temp = await self.fun.roshambo(ctx, member, False)

        if temp:
            await ctx.reply(embed=temp[0])

    @slash_command(name='random')
    async def slash_random(self, ctx):
        '''Try to guess the random number'''
        await self.fun.random(ctx, True)

    @slash_command(name='fast')
    async def slash_fast(self, ctx, lang: Option(str, 'Language you want to use', choices=['English', 'Arabic', 'Random'], required=False, default='random')):
        '''Try to type the word as fast as you can'''
        await self.fun.typing_games(ctx, lang, 'fast', True)

    @slash_command(name='spell')
    async def slash_spell(self, ctx, lang: Option(str, 'Language you want to use', choices=['English', 'Arabic', 'Random'], required=False, default='random')):
        '''Try to spell the word as fast as you can'''
        await self.fun.typing_games(ctx, lang, 'spell', True)

    @slash_command(name='say')
    async def slash_ping(self, ctx, message: Option(str, 'Message you want the bot to say')):
        '''Make the bot say something'''
        await ctx.respond(embed=create_embeds(ctx, ('', message)))

    @slash_command(name='roll')
    async def slash_roll(self, ctx, min: Option(int, 'Min number you want to start with', required=False, default=1), max: Option(int, 'Max number you want to end with', required=False, default=10)):
        '''Get a random number'''
        await ctx.respond(embed=(temp := self.fun.roll(ctx, min, max))[0], ephemeral=temp[1])

    @slash_command(name='8ball')
    async def slash_8ball(self, ctx, question: Option(str, 'Question you want to ask')):
        '''Get a random answer for your question'''
        await ctx.respond(embed=self.fun.magic_ball(ctx, question))

    @slash_command(name='choose')
    async def slash_choose(self, ctx, choices: Option(str, 'Your choices (every choice must end with `,`)')):
        '''Choose a random choice from your choices'''
        await ctx.respond(embed=self.fun.choose(ctx, choices))

    @slash_command(name='tictactoe')
    async def slash_tictactoe(self, ctx, member: Option(discord.Member, 'Member you want to play with')):
        '''Play tictactoe game with other member'''
        temp = await self.fun.tictactoe(ctx, member, True)

        if temp:
            await ctx.respond(embed=temp[0], ephemeral=temp[1])

    @slash_command(name='roshambo')
    async def slash_roshambo(self, ctx, member: Option(discord.Member, 'Member you want to play with', required=False, default=None)):
        '''Play roshambo (Rock-Paper-Scissors) game with [me, member]'''
        temp = await self.fun.roshambo(ctx, member, True)

        if temp:
            await ctx.respond(embed=temp[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(FunCommands(bot))
