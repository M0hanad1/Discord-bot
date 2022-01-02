import discord
import math
from discord.ext import commands
from src.functions.functions import Functions
from src.data.data import Data


class Score(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = Data()

    async def top_gen(self, ctx, mood, page):
        id_ = str(ctx.author.id)
        all_score = {}
        message = ''
        all_messages = []
        num = 1
        count_num = 1
        first = True

        for i in self.data.users_data:
            if ((mood == 'local' and ctx.guild.get_member(int(i)) is not None) or (mood == 'global')) and ((temp := self.data.get_score(i)) != -1):
                all_score[i] = temp

        all_score = dict(sorted(all_score.items(), key=lambda item: item[1], reverse=True))

        if page > math.ceil(len(all_score) / 10):
            page = 1

        author_data = None if id_ not in all_score else [all_score[id_], list(all_score.keys()).index(id_)+1]

        for i, j in all_score.items():
            if first:
                if author_data is not None and author_data[0] > j:
                    message += f'**{author_data[1]}- <@!{id_}>: {author_data[0]}**\n'

                first = False

            if id_ == i:
                message += f'**{num}- <@!{i}>: {j}**\n'

            else:
                message += f'{num}- <@!{i}>: {j}\n'

            num += 1
            count_num += 1

            if count_num == 11:
                if id_ not in message:
                    message += f'**{author_data[1]}- <@!{id_}>: {author_data[0]}**\n'

                count_num = 1
                first = True
                all_messages.append(message)
                message = ''

        all_messages.append(message)
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
        user_score = self.data.get_score(str(member.id))
        user_score = 0 if user_score == -1 else user_score

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'Score:\n{user_score}', ''), (member.name, member.avatar.url)))

def setup(bot: commands.Bot):
    bot.add_cog(Score(bot))
