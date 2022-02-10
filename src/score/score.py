import discord
from src.data.data import Data
from src.functions.functions import create_embeds, member_avatar, server_avatar
from discord.ext import commands


class ScoreData(Data):
    def __init__(self) -> None:
        super().__init__()

    def add_score(self, server_id, member_id, score):
        self.update_user({'_id': member_id}, {'$set': {f'score.{server_id}': score}})

    def get_user_global(self, member_id):
        result = 0

        for i in self.get_user({'_id': member_id, 'score': {'$exists': True}}):
            for j in i['score'].values():
                result += j

        return result

    def get_all_global(self):
        result = {}

        for i in self.get_user({'score': {'$exists': True}}):
            result[i['_id']] = 0

            for j in i['score'].values():
                result[i['_id']] += j

        return result

    def get_user_local(self, server_id, member_id):
        for i in self.get_user({'_id': member_id, f'score.{server_id}': {'$exists': True}}):
            return i['score'][str(server_id)]

        return 0

    def get_all_local(self, server_id):
        result = {}

        for i in self.get_user({f'score.{server_id}': {'$exists': True}}):
            result[i['_id']] = i['score'][str(server_id)]

        return result


class Score:
    def __init__(self, bot: commands.Bot) -> None:
        self.data = ScoreData()
        self.bot = bot

    async def score(self, ctx, member: discord.Member):
        member = ctx.author if member is None else member
        return create_embeds(ctx, (f'Global Score: `{self.data.get_user_global(member.id)}`\nLocal Score: `{self.data.get_user_local(ctx.guild.id, member.id)}`', ''), (member.name, member_avatar(member)))

    def get_mood(self, mood):
        if mood == 'global' or mood == 'g' or mood == 'discord' or mood == 'd':
            return 'global'

        elif mood == 'local' or mood == 'l' or mood == 'server' or mood == 's':
            return 'local'

        else:
            return 'both'

    def top(self, ctx, mood='both', page=None):
        all_local_message = []
        all_global_message = []
        local_message = ''
        global_message = ''

        if mood == 'both' or mood == 'local':
            members = self.data.get_all_local(ctx.guild.id)

            for i in members.copy():
                if not ctx.guild.get_member(i):
                    del members[i]

            temp_local = dict(sorted(members.items(), key=lambda item: item[1], reverse=True))
            score = (list(temp_local.keys()).index(ctx.author.id)+1, temp_local[ctx.author.id]) if ctx.author.id in temp_local else (len(temp_local)+1, 0)
            message_author = [str(ctx.author.id), score[0], score[1]]

            for i, j in enumerate(temp_local):
                if i == 5 and mood == 'both':
                    if message_author[0] not in local_message:
                        local_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                    break

                if i == 10 and mood == 'local':
                    if message_author[0] not in local_message:
                        local_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                    all_local_message.append(local_message)
                    local_message = ''

                if str(j) == message_author[0]:
                    local_message += f'**{i+1}- <@{j}>: {temp_local[j]}**\n'

                else:
                    if len(local_message) == 0 and i > message_author[1]-1:
                        local_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                    local_message += f'{i+1}- <@{j}>: `{temp_local[j]}`\n'

            if len(local_message) > 0 or message_author[0] not in local_message:
                if message_author[0] not in local_message:
                    local_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                if mood == 'both':
                    local_message += 'More: `top local`'

                all_local_message.append(local_message)

            if mood == 'local':
                page = 1 if (page > len(all_local_message) or page < 1) else page
                return create_embeds(ctx, (f'Top guild score [{page}/{len(all_local_message)}]:', all_local_message[page-1]), (ctx.guild.name, server_avatar(ctx.guild)))

        if mood == 'both' or mood == 'global':
            temp_global = dict(sorted(self.data.get_all_global().items(), key=lambda item: item[1], reverse=True))
            score = (list(temp_global.keys()).index(ctx.author.id)+1, temp_global[ctx.author.id]) if ctx.author.id in temp_global else (len(temp_global)+1, 0)
            message_author = [str(ctx.author.id), score[0], score[1]]

            for i, j in enumerate(temp_global):
                if i == 5 and mood == 'both':
                    if message_author[0] not in global_message:
                        global_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                    break

                if i == 10 and mood == 'global':
                    if message_author[0] not in global_message:
                        global_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                    all_global_message.append(global_message)
                    global_message = ''

                if str(j) == message_author[0]:
                    global_message += f'**{i+1}- <@{j}>: {temp_global[j]}**\n'

                else:
                    if len(global_message) == 0 and i > message_author[1]-1:
                        global_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                    global_message += f'{i+1}- <@{j}>: `{temp_global[j]}`\n'

            if len(global_message) > 0 or message_author[0] not in global_message:
                if message_author[0] not in global_message:
                    global_message += f'**{message_author[1]}- <@{message_author[0]}>: {message_author[2]}**\n'

                if mood == 'both':
                    global_message += 'More: `top global`'

                all_global_message.append(global_message)

        if mood == 'global':
            page = 1 if (page > len(all_global_message) or page < 1) else page
            return create_embeds(ctx, (f'Top global score [{page}/{len(all_global_message)}]:', all_global_message[page-1]), ('Global', 'https://www.bestappsforkids.com/wp-content/uploads/2021/10/Discord.png'))

        return create_embeds(ctx, ('Top score:', ''), (ctx.guild.name, server_avatar(ctx.guild)), embed_field=[('Local score:', local_message, True), ('Global score:', global_message, True)])

    def upgrade_score(self, ctx, member):
        self.data.add_score(ctx.guild.id, member.id, self.data.get_user_local(ctx.guild.id, member.id)+1)
