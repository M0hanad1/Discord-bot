import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from src.functions.functions import create_embeds
from src.main.main import Main
from typing import Union


class MainCommands(commands.Cog, name='Global'):
    '''Global commands'''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main = Main(self.bot)

    @commands.command(name='info', description='Get information about the bot')
    async def command_info(self, ctx):
        '''{prefix}info'''
        await ctx.reply(embed=await self.main.info(ctx))

    @commands.command(name='user', description='Get information about member')
    async def command_user(self, ctx, member: discord.Member=None):
        '''{prefix}user
        {prefix}user {mention}'''
        await ctx.reply(embed=await self.main.user(ctx, member))

    @commands.command(name='banner', description='Get member profile banner')
    async def command_banner(self, ctx, member: discord.Member=None):
        '''{prefix}banner
        {prefix}banner {mention}'''
        await ctx.reply(embed=(await self.main.banner(ctx, member))[0])

    @commands.command(name='avatar', description='Get member profile avatar')
    async def command_avatar(self, ctx, member: discord.Member=None):
        '''{prefix}avatar
        {prefix}avatar {mention}'''
        await ctx.reply(embed=self.main.avatar(ctx, member))

    @commands.command(name='server', description='Get information about the server')
    async def command_server(self, ctx):
        '''{prefix}server'''
        await ctx.reply(embed=self.main.server(ctx))

    @commands.command(name='ping', description='Get the legacy ping')
    async def command_ping(self, ctx):
        '''{prefix}ping'''
        await ctx.reply(embed=self.main.ping(ctx))

    @commands.command(name='emoji', description='Get emoji link by using the [emoji, id]')
    async def command_emoji(self, ctx, emoji: Union[discord.Emoji, int]):
        '''{prefix}emoji <:emoji_1:843168750320353291>
        {prefix}emoji 843168750320353291'''
        await ctx.reply(embed=self.main.get_emoji(ctx, emoji)[0])

    @commands.command(name='calculate', aliases=['calc'], description='Calculate a math calculation')
    async def command_calc(self, ctx, *, calculation: str):
        '''{prefix}calculation 1+1
        {prefix}calculate (1+1)x5x150/20-6'''
        await ctx.reply(embed=self.main.calc(ctx, calculation)[0])

    @commands.command(name='search', description='Search for something in google')
    async def command_search(self, ctx, *, item: str):
        '''{prefix}search Celeste Steam
        {prefix}search Youtube'''
        temp = await ctx.reply(embed=create_embeds(ctx, ('Searching...', '')))
        await temp.edit(embed=self.main.search(ctx, item)[0])

    @commands.command(name='icon', description='Get server icon')
    async def command_icon(self, ctx):
        '''{prefix}icon'''
        await ctx.reply(embed=self.main.icon(ctx)[0])

    @commands.command(name='translate', aliases=['trans'], description='Translate text to default server language')
    async def command_trans(self, ctx, *, text):
        '''{prefix}translate こんにちは
        {prefix}translate Водка'''
        temp = await ctx.reply(embed=create_embeds(ctx, ('Translating...', '')))
        await temp.edit(embed=self.main.trans(ctx, text)[0])

    @slash_command(name='info')
    async def slash_info(self, ctx):
        '''Get information about the bot'''
        await ctx.respond(embed=await self.main.info(ctx))

    @slash_command(name='user')
    async def slash_user(self, ctx, member: Option(discord.Member, 'Member you want to get information about', required=False, default=None)):
        '''Get information about member'''
        await ctx.respond(embed=await self.main.user(ctx, member))

    @slash_command(name='banner')
    async def slash_banner(self, ctx, member: Option(discord.Member, 'Member you want to get information about', required=False, default=None)):
        '''Get member profile banner'''
        await ctx.respond(embed=(temp := (await self.main.banner(ctx, member)))[0], ephemeral=temp[1])

    @slash_command(name='avatar')
    async def slash_avatar(self, ctx, member: Option(discord.Member, 'Member you want to get avatar of', required=False, default=None)):
        '''To get member avatar'''
        await ctx.respond(embed=self.main.avatar(ctx, member))

    @slash_command(name='server')
    async def slash_server(self, ctx):
        '''Get information about the server'''
        await ctx.respond(embed=self.main.server(ctx))

    @slash_command(name='ping')
    async def slash_ping(self, ctx):
        '''Get the legacy ping'''
        await ctx.respond(embed=self.main.ping(ctx))

    @slash_command(name='emoji')
    async def slash_emoji(self, ctx, emoji: Option(str, 'Emoji you want to get')):
        '''Get emoji link by using the [emoji, id]'''
        if emoji.isdigit():
            emoji = int(emoji)

        else:
            converter = commands.EmojiConverter()
            emoji = await converter.convert(ctx, emoji)

        await ctx.respond(embed=(temp := self.main.get_emoji(ctx, emoji))[0], ephemeral=temp[1])

    @slash_command(name='calculate')
    async def slash_calc(self, ctx, calculation: Option(str, 'Calculation you want to do')):
        '''Calculate a math calculation'''
        await ctx.respond(embed=(temp := self.main.calc(ctx, calculation))[0], ephemeral=temp[1])

    @slash_command(name='search')
    async def slash_search(self, ctx, item: Option(str, 'Item you want to search for')):
        '''Search for something in google'''
        await ctx.defer()
        await ctx.respond(embed=(temp := self.main.search(ctx, item))[0], ephemeral=temp[1])

    @slash_command(name='icon')
    async def slash_icon(self, ctx):
        '''Get server icon'''
        await ctx.respond(embed=(temp := self.main.icon(ctx))[0], ephemeral=temp[1])

    @slash_command(name='translate')
    async def slash_trans(self, ctx, text: Option(str, 'Text you want to convert from'), from_: Option(str, 'Language you want to translate from', required='False', default='auto', name='from'), to: Option(str, 'Language you want to translate to', required=False, default=None)):
        '''Translate text'''
        await ctx.defer()
        await ctx.respond(embed=(temp := self.main.trans(ctx, text, from_, to))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot))
