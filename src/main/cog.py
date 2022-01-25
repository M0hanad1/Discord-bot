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

    @commands.command(name='info')
    async def command_info(self, ctx):
        '''To get information about the bot'''
        await ctx.reply(embed=await self.main.info(ctx))

    @commands.command(name='user')
    async def command_user(self, ctx, member: discord.Member=None):
        '''To get information about member'''
        await ctx.reply(embed=await self.main.user(ctx, member))

    @commands.command(name='banner')
    async def command_banner(self, ctx, member: discord.Member=None):
        '''To get member banner'''
        await ctx.reply(embed=(await self.main.banner(ctx, member))[0])

    @commands.command(name='avatar')
    async def command_avatar(self, ctx, member: discord.Member=None):
        '''To get member avatar'''
        await ctx.reply(embed=self.main.avatar(ctx, member))

    @commands.command(name='server')
    async def command_server(self, ctx):
        '''To get information about the server with perfix command'''
        await ctx.reply(embed=self.main.server(ctx))

    @commands.command(name='ping')
    async def command_ping(self, ctx):
        '''To get the ping'''
        await ctx.reply(embed=self.main.ping(ctx))

    @commands.command(name='emoji')
    async def command_emoji(self, ctx, emoji: Union[discord.Emoji, int]):
        '''To get emoji link'''
        await ctx.reply(embed=self.main.get_emoji(ctx, emoji)[0])

    @commands.command(name='calc')
    async def command_calc(self, ctx, *, calculation: str):
        '''To calculate a calculation'''
        await ctx.reply(embed=self.main.calc(ctx, calculation)[0])

    @commands.command(name='search')
    async def command_search(self, ctx, *, item: str):
        '''To search for something in google'''
        temp = await ctx.reply(embed=create_embeds(ctx, ('Searching...', '')))
        await temp.edit(embed=self.main.search(ctx, item)[0])

    @commands.command(name='icon')
    async def command_icon(self, ctx):
        '''To get server icon'''
        await ctx.reply(embed=self.main.icon(ctx)[0])

    @commands.command(name='translate', aliases=['trans'])
    async def command_trans(self, ctx, *, text):
        '''To translate text'''
        await ctx.reply(embed=self.main.trans(ctx, text)[0])

    @slash_command(name='info')
    async def slash_info(self, ctx):
        '''To get information about the bot'''
        await ctx.respond(embed=await self.main.info(ctx))

    @slash_command(name='user')
    async def slash_user(self, ctx, member: Option(discord.Member, 'Member you want to get information about', required=False, default=None)):
        '''To get information about member'''
        await ctx.respond(embed=await self.main.user(ctx, member))

    @slash_command(name='banner')
    async def slash_banner(self, ctx, member: Option(discord.Member, 'Member you want to get information about', required=False, default=None)):
        '''To get member banner'''
        await ctx.respond(embed=(temp := (await self.main.banner(ctx, member)))[0], ephemeral=temp[1])

    @slash_command(name='avatar')
    async def slash_avatar(self, ctx, member: Option(discord.Member, 'Member you want to get avatar of', required=False, default=None)):
        '''To get member avatar'''
        await ctx.respond(embed=self.main.avatar(ctx, member))

    @slash_command(name='server')
    async def slash_server(self, ctx):
        '''To get information about the server'''
        await ctx.respond(embed=self.main.server(ctx))

    @slash_command(name='ping')
    async def slash_ping(self, ctx):
        '''To get the ping'''
        await ctx.respond(embed=self.main.ping(ctx))

    @slash_command(name='emoji')
    async def slash_emoji(self, ctx, emoji: Option(str, 'Emoji you want to get')):
        '''To get emoji link'''
        if emoji.isdigit():
            emoji = int(emoji)

        else:
            converter = commands.EmojiConverter()
            emoji = await converter.convert(ctx, emoji)

        await ctx.respond(embed=(temp := self.main.get_emoji(ctx, emoji))[0], ephemeral=temp[1])

    @slash_command(name='calc')
    async def slash_calc(self, ctx, calculation: Option(str, 'Calculation you want to do')):
        '''To calculate a calculation'''
        await ctx.respond(embed=(temp := self.main.calc(ctx, calculation))[0], ephemeral=temp[1])

    @slash_command(name='search')
    async def slash_search(self, ctx, item: Option(str, 'Item you want to search for')):
        '''To search for something in google'''
        await ctx.defer()
        await ctx.respond(embed=(temp := self.main.search(ctx, item))[0], ephemeral=temp[1])

    @slash_command(name='icon')
    async def slash_icon(self, ctx):
        '''To get server icon'''
        await ctx.respond(embed=(temp := self.main.icon(ctx))[0], ephemeral=temp[1])

    @slash_command(name='translate')
    async def slash_trans(self, ctx, text: Option(str, 'Text you want to convert from'), from_: Option(str, 'Language you want to translate from', required='False', default='auto', name='from'), to: Option(str, 'Language you want to translate to', required=False, default=None)):
        '''To translate text'''
        await ctx.respond(embed=(temp := self.main.trans(ctx, text, from_, to))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot))
