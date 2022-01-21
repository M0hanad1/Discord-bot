import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from src.main.main import Main
from typing import Union


class MainCommands(commands.Cog, name='Main'):
    """Main commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main = Main(self.bot)

    @commands.command(name='info')
    async def command_info(self, ctx):
        """To get information about the bot with prefix command"""
        await ctx.reply(embed=await self.main.info(ctx))

    @commands.command(name='user')
    async def command_user(self, ctx, member: discord.Member=None):
        """To get information about member with prefix command"""
        await ctx.reply(embed=await self.main.user(ctx, member))

    @commands.command(name='banner')
    async def command_banner(self, ctx, member: discord.Member=None):
        """To get member banner with prefix command"""
        await ctx.reply(embed=(await self.main.banner(ctx, member))[0])

    @commands.command(name='avatar')
    async def command_avatar(self, ctx, member: discord.Member=None):
        """To get member avatar with prefix command"""
        await ctx.reply(embed=self.main.avatar(ctx, member))

    @commands.command(name='server')
    async def command_server(self, ctx):
        """To get information about the server with perfix command"""
        await ctx.reply(embed=self.main.server(ctx))

    @commands.command(name='ping')
    async def command_ping(self, ctx):
        """To get the ping with prefix command"""
        await ctx.reply(embed=self.main.ping(ctx))

    @commands.command(name='emoji')
    async def command_emoji(self, ctx, emoji: Union[discord.Emoji, int]):
        """To get emoji link with prefix command"""
        await ctx.reply(embed=self.main.get_emoji(ctx, emoji)[0])

    @commands.command(name='calc')
    async def command_calc(self, ctx, *, calculation: str):
        """To calculate a calculation with prefix command"""
        await ctx.reply(embed=self.main.calc(ctx, calculation)[0])

    @slash_command(name='info')
    async def slash_info(self, ctx):
        """To get information about the bot with slash command"""
        await ctx.respond(embed=await self.main.info(ctx))

    @slash_command(name='user')
    async def slash_user(self, ctx, member: Option(discord.Member, 'Member you want to get information about', required=False, default=None)):
        """To get information about member with slash command"""
        await ctx.respond(embed=await self.main.user(ctx, member))

    @slash_command(name='banner')
    async def slash_banner(self, ctx, member: Option(discord.Member, 'Member you want to get information about', required=False, default=None)):
        """To get member banner with slash command"""
        await ctx.respond(embed=(temp := (await self.main.banner(ctx, member)))[0], ephemeral=temp[1])

    @slash_command(name='avatar')
    async def slash_avatar(self, ctx, member: Option(discord.Member, 'Member you want to get avatar of', required=False, default=None)):
        """To get member avatar with slash command"""
        await ctx.respond(embed=self.main.avatar(ctx, member))

    @slash_command(name='server')
    async def slash_server(self, ctx):
        """To get information about the server with slash command"""
        await ctx.respond(embed=self.main.server(ctx))

    @slash_command(name='ping')
    async def slash_ping(self, ctx):
        """To get the ping with prefix command"""
        await ctx.respond(embed=self.main.ping(ctx))

    @slash_command(name='emoji')
    async def slash_emoji(self, ctx, emoji: Option(str, 'Emoji you want to get')):
        """To get emoji link with slash command"""
        if emoji.isdigit():
            emoji = int(emoji)

        else:
            converter = commands.EmojiConverter()
            emoji = await converter.convert(ctx, emoji)

        await ctx.respond(embed=(temp := self.main.get_emoji(ctx, emoji))[0], ephemeral=temp[1])

    @slash_command(name='calc')
    async def slash_calc(self, ctx, calculation: Option(str, 'Calculation you want to do')):
        """To calculate a calculation with slash command"""
        await ctx.respond(embed=(temp := self.main.calc(ctx, calculation))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(MainCommands(bot))
