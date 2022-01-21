import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from typing import Union
from src.score.score import Score
from src.functions.functions import *


class ScoreCommands(commands.Cog, name='Score'):
    """Score commands"""
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = Score(self.bot)

    # async def top_gen(self, ctx, mood, page):
    #     scores = dict(sorted(self.data.get_all_score().items(), key=lambda item: item[1], reverse=True))
    #     temp = scores.copy()

    #     if mood == 'local':
    #         for i in scores:
    #             if ctx.guild.get_member(i) is None:
    #                 del temp[i]

    #     scores = temp

    #     if ctx.author.id not in scores:
    #         scores[ctx.author.id] = 0

    #     author_data = [ctx.author.id, list(scores.keys()).index(ctx.author.id)+1, scores[ctx.author.id]]
    #     num = 1
    #     count = 1
    #     message = ''
    #     all_messages = []

    #     for i, j in scores.items():
    #         if count == 10:
    #             if str(author_data[0]) not in message:
    #                 if author_data[1] < num:
    #                     message = f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**' + message

    #                 else:
    #                     message += f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**'

    #             all_messages.append(message)
    #             count = 1
    #             message = ''

    #         if author_data[0] == i:
    #             message += f'**{num}- <@{i}>: {j}**\n'

    #         else:
    #             message += f'{num}- <@{i}>: {j}\n'

    #         num += 1
    #         count += 1

    #     if len(message) > 0:
    #         if str(author_data[0]) not in message:
    #                 if author_data[1] < num:
    #                     message = f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**' + message

    #                 else:
    #                     message += f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**'

    #         all_messages.append(message)

    #     if page > len(all_messages):
    #         page = 1

    #     await ctx.reply(embed=create_embeds(ctx, (f'Top {mood} score [{page} | {len(all_messages)}]:', all_messages[page-1])))

    @commands.command(name='top')
    async def command_top(self, ctx, mood: str='both', page: int=1):
        """To get top [global | local | both] score with prefix command"""
        await ctx.reply(embed=self.data.top(ctx, self.data.get_mood(mood.lower()), page))

    @commands.command(name='score')
    async def command_score(self, ctx, *, member: str=None):
        """To get [your | member] score with prefix command"""
        await ctx.reply(embed=await self.data.score(ctx, member))

    @slash_command(name='score')
    async def slash_score(self, ctx, member: Option(discord.Member, 'Member you want to see his score', required=False, default=None)):
        """To get [your|member] score with slash command"""
        await ctx.respond(embed=await self.data.score(ctx, member))

    @slash_command(name='top')
    async def slash_top(self, ctx, mood: Option(str, 'Choose to display [Global | Local | Both] score', choices=['Global', 'Local', 'Both'], required=False, default='both'), page: Option(int, 'Page you want to display', required=False, default=1)):
        """To get top [global | local | both] score with prefix command"""
        await ctx.respond(embed=self.data.top(ctx, self.data.get_mood(mood.lower()), page))


def setup(bot: commands.Bot):
    bot.add_cog(ScoreCommands(bot))
