import discord
from discord.ext import commands
from requests import get
from bs4 import BeautifulSoup
from src.functions import create_embeds, member_avatar, get_banner, server_avatar
from string import digits
from googlesearch import search


class Main:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def info(self, ctx):
        return create_embeds(ctx, embed_author=(self.bot.user.name, member_avatar(self.bot.user)), embed_field=[('Bot:', self.bot.user.mention, False), ('Prefix:', f'**{(await self.bot.get_prefix(ctx))[-1]}**', False), ('Developer:', '<@589198370111881216>', False)])

    async def banner(self, ctx, member):
        member = ctx.author if member is None else member

        if (banner := await get_banner(self.bot, member)) is None:
            return (create_embeds(ctx, ('This member has no banner', '')), True)

        return (create_embeds(ctx, ('', f'**[Banner Link]({banner})**'), (member.name, member_avatar(member)), embed_image=banner), False)

    def get_emoji(self, ctx, emoji: discord.Emoji):
        if isinstance(emoji, int):
            if get(f'https://cdn.discordapp.com/emojis/{emoji}.gif').status_code != 200:
                if get(f'https://cdn.discordapp.com/emojis/{emoji}.png').status_code != 200:
                    return (create_embeds(ctx, ('I can\'t find this emoji', '')), True)

                else:
                    url = f'https://cdn.discordapp.com/emojis/{emoji}.png'

            else:
                url = f'https://cdn.discordapp.com/emojis/{emoji}.gif'

        else:
            url = emoji.url

        return (create_embeds(ctx, ('', f'**[Emoji Link]({url})**'), embed_image=url), False)

    async def user(self, ctx, member: discord.Member):
        member = ctx.author if member is None else member
        role = 'No roles' if len(role := ' '.join([i.mention for i in member.roles if i.name not in '@everyone'])) == 0 else role
        avatar = member_avatar(member)
        message = '' if (banner := await get_banner(self.bot, member)) is None else f', **[Banner]({banner})**'
        return create_embeds(ctx, ('', f'**[Avatar]({avatar})**{message}'), (member.name, avatar), thumbnail=avatar, embed_field=[('Member:', member.mention, True), ('Joined at:', f'<t:{int(member.joined_at.timestamp())}:R>', True), ('Created at:', f'<t:{int(member.created_at.timestamp())}:R>', True), ('Roles:', role, True)])

    def avatar(self, ctx, member: discord.Member):
        member = ctx.author if member is None else member
        avatar = member_avatar(member)
        return create_embeds(ctx, ('', f'**[Avatar Link]({avatar})**'), (member.name, avatar), embed_image=avatar)

    def server(self, ctx):
        guild = ctx.guild
        message = '' if len(icon := server_avatar(guild)) == 0 else f'**[Server Icon]({icon})**'
        return create_embeds(ctx, ('', message), (guild.name, icon), thumbnail=icon, embed_field=[('Owner:', guild.owner.mention, True), ('Created at:', f'<t:{int(guild.created_at.timestamp())}:R>', True), (f'Members:', f'Number: {guild.member_count}\nBoosts: {guild.premium_subscription_count}', True), ('Roles:', len(guild.roles)-1, True), ('Emojis:', len(guild.emojis), True), (f'Channels ({len(guild.text_channels) + len(guild.voice_channels)}):', f'Text: {len(guild.text_channels)}\nVoice: {len(guild.voice_channels)}', True)])

    def ping(self, ctx):
        return create_embeds(ctx, (f'Your ping: {round(self.bot.latency * 1000)} ms', ''))

    def calc(self, ctx, calculation):
        for i in calculation.replace(' ', ''):
            if i not in digits + '()./*+-':
                return (create_embeds(ctx, ('Syntax error', '')), True)

        try:
            return (create_embeds(ctx, (f'Result:\n{eval(calculation)}', '')), False)

        except ZeroDivisionError:
            return (create_embeds(ctx, ('Zero division error\nCan\'t division by zero', '')), True)

        except:
            return (create_embeds(ctx, ('Syntax error', '')), True)

    def search(self, ctx, item):
        result = search(item, safe='on', num=1)

        for i in result:
            soup = BeautifulSoup(get(i).text, 'html.parser')
            title = soup.title.string
            desc = soup.find('meta', attrs={'name': 'description'})
            desc = desc if desc else soup.find('meta', property='og:description')
            return (create_embeds(ctx, ('Result:', f'**[Website]({i})**'), embed_field=[('Title:', f'**[{title}]({i})**' if title else '**No title found**', False), ('Description:', f'```\n{desc["content"]}```' if desc else '**No description found***', False)]), False)

        return (create_embeds(ctx, ('No result found', '')), True)

    def icon(self, ctx):
        if len(icon := server_avatar(ctx.guild)) == 0:
            return (create_embeds(ctx, ('This server has no icon', '')), True)

        return (create_embeds(ctx, ('', f'**[Icon Link]({icon})**'), (ctx.guild.name, icon), embed_image=icon), False)
