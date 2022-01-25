import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from src.score.score import Score


class ScoreCommands(commands.Cog, name='Score'):
    '''Score commands'''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = Score(self.bot)

    @commands.command(name='top')
    async def command_top(self, ctx, mood: str='both', page: int=1):
        '''To get top [global | local | both] score'''
        await ctx.reply(embed=self.data.top(ctx, self.data.get_mood(mood.lower()), page))

    @commands.command(name='score')
    async def command_score(self, ctx, *, member: discord.Member=None):
        '''To get [your | member] score'''
        await ctx.reply(embed=await self.data.score(ctx, member))

    @slash_command(name='score')
    async def slash_score(self, ctx, member: Option(discord.Member, 'Member you want to see his score', required=False, default=None)):
        '''To get [your|member] score'''
        await ctx.respond(embed=await self.data.score(ctx, member))

    @slash_command(name='top')
    async def slash_top(self, ctx, mood: Option(str, 'Choose to display [Global | Local | Both] score', choices=['Global', 'Local', 'Both'], required=False, default='both'), page: Option(int, 'Page you want to display', required=False, default=1)):
        '''To get top [global | local | both] score'''
        await ctx.respond(embed=self.data.top(ctx, mood.lower(), page))


def setup(bot: commands.Bot):
    bot.add_cog(ScoreCommands(bot))
