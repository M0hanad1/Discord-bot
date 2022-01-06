import discord
from discord.ext import commands
from src.functions.functions import Functions
from src.score.score import ScoreData


class Score(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = ScoreData()

    async def top_gen(self, ctx, mood, page):
        scores = dict(sorted(self.data.get_all_score().items(), key=lambda item: item[1], reverse=True))
        temp = scores.copy()

        if mood == 'local':
            for i in scores:
                if ctx.guild.get_member(i) is None:
                    del temp[i]

        scores = temp

        if ctx.author.id not in scores:
            scores[ctx.author.id] = 0

        author_data = [ctx.author.id, list(scores.keys()).index(ctx.author.id)+1, scores[ctx.author.id]]
        num = 1
        count = 1
        message = ''
        all_messages = []

        for i, j in scores.items():
            if count == 10:
                if str(author_data[0]) not in message:
                    if author_data[1] < num:
                        message = f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**' + message

                    else:
                        message += f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**'

                all_messages.append(message)
                count = 1
                message = ''

            if author_data[0] == i:
                message += f'**{num}- <@{i}>: {j}**\n'

            else:
                message += f'{num}- <@{i}>: {j}\n'

            num += 1
            count += 1

        if len(message) > 0:
            if str(author_data[0]) not in message:
                    if author_data[1] < num:
                        message = f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**' + message

                    else:
                        message += f'**{author_data[1]}- <@{author_data[0]}>: {author_data[2]}\n**'

            all_messages.append(message)

        if page > len(all_messages):
            page = 1

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'Top {mood} score [{page} | {len(all_messages)}]:', all_messages[page-1])))

    @commands.command(name='top', aliases=['top-u', 'top-l', 'top-user', 'top-local'])
    async def top_local(self, ctx, page=1):
        await self.top_gen(ctx, 'local', page)

    @commands.command(name='top-server', aliases=['top-s', 'top-g', 'top-global'])
    async def top_global(self, ctx, page=1):
        await self.top_gen(ctx, 'global', page)

    @commands.command()
    async def score(self, ctx, member: discord.Member=None):
        member = ctx.author if member is None else member

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'Score:\n{self.data.get_score(member.id)}', ''), (member.name, member.avatar.url)))

def setup(bot: commands.Bot):
    bot.add_cog(Score(bot))
