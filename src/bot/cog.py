import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from src.bot.bot_info import BotInfo


class BotInfoCommands(commands.Cog, name='Bot'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot_info = BotInfo(self.bot)

    @commands.command(name='info', description='Get information about the bot')
    async def command_info(self, ctx):
        '''{prefix}info'''
        await ctx.reply(embed=await self.bot_info.info(ctx))

    @commands.command(name='invite', description='Get bot invite link')
    async def command_invite(self, ctx):
        '''{prefix}invite'''
        await ctx.reply(embed=self.bot_info.invite(ctx))

    @commands.command(name='vote', description='Get bot vote link in top.gg')
    async def command_vote(self, ctx):
        '''{prefix}vote'''
        await ctx.reply(embed=self.bot_info.vote(ctx))

    @commands.command(name='developer', aliases=['dev'], description='Get the developer of the bot')
    async def command_dev(self, ctx):
        '''{prefix}developer'''
        await ctx.reply(embed=await self.bot_info.dev(ctx))

    @commands.command(name='updates', aliases=['update', 'up'], description='[Show, Add, Remove] bot updates & new features channel')
    @commands.has_permissions(manage_guild=True)
    async def command_updates(self, ctx, channel: discord.TextChannel=None, *, message: str=None):
        '''{prefix}updates
        {prefix}updates {text_channel}
        {prefix}updates {text_channel} {role} New update
        
        Note: if you set the `message` to `None`, that will remove the message'''
        await ctx.reply(embed=(await self.bot_info.updates(ctx, channel, message))[0])

    @commands.command(name='send', description='Send bot update message to all the server', hidden=True)
    async def command_send(self, ctx, title='', description='', *, fields='None'):
        '''{prefix}send [('New', 'New feature', False), ('update', 'new update', True)]'''
        if ctx.author.id == self.bot.owner_id:
            await self.bot_info.send_updates(ctx, title, description, fields)

    @slash_command(name='info')
    async def slash_info(self, ctx):
        '''Get information about the bot'''
        await ctx.respond(embed=await self.bot_info.info(ctx))

    @slash_command(name='invite')
    async def slash_invite(self, ctx):
        '''Get bot invite link'''
        await ctx.respond(embed=self.bot_info.invite(ctx))

    @slash_command(name='vote')
    async def slash_vote(self, ctx):
        '''Get bot vote link in top.gg'''
        await ctx.respond(embed=self.bot_info.vote(ctx))

    @slash_command(name='developer')
    async def slash_dev(self, ctx):
        '''Get the developer of the bot'''
        await ctx.respond(embed=await self.bot_info.dev(ctx))

    @slash_command(name='updates', guild_ids=[934444583998353489])
    @commands.has_permissions(manage_guild=True)
    async def slash_updates(self, ctx, channel: Option(discord.TextChannel, 'Channel you want to [add to, remove from] bot updates & new features', required=False, default=None), message: Option(str, 'Message you want to [send with, remove from] bot update message (Write `None` to remove it)', required=False, default=None)):
        '''[Show, Add, Remove] bot updates & new features channel'''
        await ctx.respond(embed=(temp := (await self.bot_info.updates(ctx, channel, message)))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(BotInfoCommands(bot))
