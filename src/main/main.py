import discord
from discord.ext import commands
from requests import get
from bs4 import BeautifulSoup
from src.functions import create_embeds, get_banner, server_avatar
from string import digits
from googlesearch import search
from googletrans import Translator


class Main:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def info(self, ctx):
        return create_embeds(ctx, embed_author=(self.bot.user.name, self.bot.user.display_avatar), embed_field=[('Bot:', self.bot.user.mention, False), ('Prefix:', f'**{(await self.bot.get_prefix(ctx))[-1]}**', False), ('Developer:', '<@589198370111881216>', False)])

    async def banner(self, ctx, member):
        member = ctx.author if member is None else member

        if (banner := await get_banner(self.bot, member)) is None:
            return (create_embeds(ctx, ('This member has no banner', '')), True)

        return (create_embeds(ctx, ('', f'**[Banner Link]({banner})**'), (member.name, member.display_avatar), embed_image=banner), False)

    def get_emoji(self, ctx, emoji: discord.Emoji):
        if emoji.isdigit():
            emoji = int(emoji)

        else:
            try:
                emoji = int(emoji.split(':')[2][:-1])

            except:
                raise commands.EmojiNotFound(emoji)

        if get(f'https://cdn.discordapp.com/emojis/{emoji}.gif').status_code != 200:
            if get(f'https://cdn.discordapp.com/emojis/{emoji}.png').status_code != 200:
                raise commands.EmojiNotFound(str(emoji))

            else:
                url = f'https://cdn.discordapp.com/emojis/{emoji}.png'

        else:
            url = f'https://cdn.discordapp.com/emojis/{emoji}.gif'

        return (create_embeds(ctx, ('', f'**[Emoji Link]({url})**'), embed_image=url), False)

    async def user(self, ctx, member: discord.Member):
        member = ctx.author if member is None else member
        role = '`No roles`' if len(role := '**, **'.join([i.mention for i in member.roles[::-1] if i.name not in '@everyone'])) == 0 else role
        avatar = member.display_avatar
        message = '' if (banner := await get_banner(self.bot, member)) is None else f', **[Banner]({banner})**'
        invites = 0

        for i in await ctx.guild.invites():
            if i.inviter == member:
                invites += i.uses

        return create_embeds(ctx, ('', f'**[Avatar]({avatar})**{message}'), (member.name, avatar), thumbnail=avatar, embed_field=[
            ('Member:', member.mention, True),
            ('Joined at:', f'<t:{int(member.joined_at.timestamp())}:R>', True),
            ('Created at:', f'<t:{int(member.created_at.timestamp())}:R>', True),
            ('ID:', f'`{member.id}`', True),
            ('Invites:', f'`{invites}`', True),
            ('Roles:', role, False)
            ])

    def avatar(self, ctx, member: discord.Member):
        member = ctx.author if member is None else member
        avatar = member.display_avatar
        return create_embeds(ctx, ('', f'**[Avatar Link]({avatar})**'), (member.name, avatar), embed_image=avatar)

    def server(self, ctx):
        guild: discord.Guild = ctx.guild
        message = '' if len(icon := server_avatar(guild)) == 0 else f'**[Server Icon]({icon})**'
        humands, bots = 0, 0
        animated, regular = 0, 0

        for i in guild.members:
            if i.bot:
                bots += 1

            else:
                humands += 1

        for i in guild.emojis:
            if i.animated:
                animated += 1

            else:
                regular += 1

        return create_embeds(ctx, ('', message), (guild.name, icon), thumbnail=icon, embed_field=[
            ('ID:', f'`{guild.id}`', True), 
            ('Created at:', f'<t:{int(guild.created_at.timestamp())}:R>', True),
            ('Owner:', guild.owner.mention, True),
            (f'Members (`{guild.member_count}`):', f'Humans: `{humands}`\nBots: `{bots}`\nBoosts: `{guild.premium_subscription_count}`', True),
            (f'Emojis (`{len(guild.emojis)}`):', f'Animated: `{animated}`\nRegular: `{regular}`', True),
            (f'Channels (`{len(guild.text_channels) + len(guild.voice_channels)}`):', f'Text: `{len(guild.text_channels)}`\nVoice: `{len(guild.voice_channels)}`', True),
            ('Roles:', f'`{len(guild.roles)-1}`', True)
            ])

    def ping(self, ctx):
        return create_embeds(ctx, (f'Your ping: `{round(self.bot.latency * 1000)}ms`', ''))

    def calc(self, ctx, calculation):
        calculation = calculation.lower().replace(' ', '').replace('x', '*')

        for i in calculation:
            if i not in digits + '()./*+-':
                return (create_embeds(ctx, ('Syntax error', '')), True)

        try:
            return (create_embeds(ctx, ('Result:', f'```\n{eval(calculation)}```')), False)

        except ZeroDivisionError:
            return (create_embeds(ctx, ('Zero division error\nCan\'t division by zero', '')), True)

        except:
            return (create_embeds(ctx, ('Syntax error', '')), True)

    def search(self, ctx, item):
        result = search(item, safe='on', num=1)

        for i in result:
            soup = BeautifulSoup(get(i).text, 'html.parser')
            title = soup.title.string
            title = title if title else soup.find('meta', property='og:title')
            desc = soup.find('meta', attrs={'name': 'description'})
            desc = desc if desc else soup.find('meta', property='og:description')
            return (create_embeds(ctx, ('Result:', f'**[Website]({i})**'), embed_field=[('Title:', f'**[{title}]({i})**' if title else '**No title found**', False), ('Description:', f'```\n{desc["content"]}```' if desc else '**No description found**', False)]), False)

        return (create_embeds(ctx, ('No result found', '')), True)

    def icon(self, ctx):
        if len(icon := server_avatar(ctx.guild)) == 0:
            return (create_embeds(ctx, ('This server has no icon', '')), True)

        return (create_embeds(ctx, ('', f'**[Icon Link]({icon})**'), (ctx.guild.name, icon), embed_image=icon), False)

    def trans(self, ctx, text, from_='auto', to=None):
        to = to if to else ctx.guild.preferred_locale.split('-')[0]

        try:
            result = Translator().translate(text, dest=to, src=from_)

        except ValueError:
            return (create_embeds(ctx, ('I can\'t find this language', '**Send a valid [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) language code**')), True)

        return (create_embeds(ctx, embed_field=[(f'From ({result.src}):', f'```\n{result.origin}```', False), (f'To ({result.dest}):', f'```\n{result.text}```', False)]), False)
