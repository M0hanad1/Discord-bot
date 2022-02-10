import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from src.moderators.mods import Mods
from typing import Union
from src.handler.handler import Handler


class ModsCommands(commands.Cog, name='Mods'):
    '''Moderations commands'''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.mod = Mods(self.bot)
        self.handler = Handler()

    @staticmethod
    def clear_check(member, role=None):
        if member is not None:
            return ['member', member]

        elif role is not None:
            return ['role', role]

        else:
            return None

    @staticmethod
    def lock_check(ctx, channel):
        return ctx.channel if channel is None else channel

    @commands.command(name='kick', description='Kick member from the server')
    @commands.has_permissions(kick_members=True)
    async def command_kick(self, ctx, member: discord.Member, *, reason='No reason'):
        '''{prefix}kick {mention}
        {prefix}kick {mention} Spamming'''
        await ctx.reply(embed=(await self.mod.kick(ctx, member, reason))[0])

    @commands.command(name='ban', description='Ban member from the server')
    @commands.has_permissions(ban_members=True)
    async def command_ban(self, ctx, member: Union[int, discord.Member], *, reason='No reason'):
        '''{prefix}ban {mention}
        {prefix}ban {id}
        {prefix}ban {mention} Swearing'''
        await ctx.reply(embed=(await self.mod.ban(ctx, member, reason))[0])

    @commands.command(name='unban', description='Unban member from the server')
    @commands.has_permissions(ban_members=True)
    async def command_unban(self, ctx, *, member: str):
        '''{prefix}unban {full_name}
        {prefix}unban {id}'''
        await ctx.reply(embed=(await self.mod.unban(ctx, member))[0])

    @commands.command(name='mute', description='Mute member (with timeout)')
    @commands.has_permissions(moderate_members=True)
    async def command_mute(self, ctx, member: discord.Member, time='3h', *, reason='No reason'):
        '''{prefix}mute {mention}
        {prefix}mute {mention} 1d
        {prefix}mute {mention} 3w Spamming'''
        await ctx.reply(embed=(await self.mod.mute(ctx, member, time, reason))[0])

    @commands.command(name='unmute', description='Unmute member (from timeout)')
    @commands.has_permissions(moderate_members=True)
    async def command_unmute(self, ctx, member: discord.Member, *, reason='No reason'):
        '''{prefix}unmute {mention}
        {prefix}unmute {mention} Wrong report'''
        await ctx.reply(embed=(await self.mod.mute(ctx, member, reason=reason, mood=False))[0])

    @commands.command(name='lock', description='Lock a text channel')
    @commands.has_permissions(manage_channels=True)
    async def command_lock(self, ctx, channel: discord.TextChannel=None):
        '''{prefix}lock
        {prefix}lock {text_channel}'''
        await ctx.reply(embed=(await self.mod.lock(ctx, self.lock_check(ctx, channel), 'lock'))[0])

    @commands.command(name='unlock', description='Unlock a text channel')
    @commands.has_permissions(manage_channels=True)
    async def command_unlock(self, ctx, channel: discord.TextChannel=None):
        '''{prefix}unlock
        {prefix}unlock {text_channel}'''
        await ctx.reply(embed=(await self.mod.lock(ctx, self.lock_check(ctx, channel), 'unlock'))[0])

    @commands.command(name='clear', description='Delete messages from the channel')
    @commands.has_permissions(manage_messages=True)
    async def command_clear(self, ctx, amount: int=25):
        '''{prefix}clear
        {prefix}clear 50'''
        await self.mod.clear(ctx, amount, None, False)

    @commands.command(name='nickname', aliases=['nick'], description='Change member nickname')
    async def command_nick(self, ctx, member: discord.Member, *, name=None):
        '''{prefix}nickname {mention}
        {prefix}nickname {mention} Nickname'''
        await ctx.reply(embed=(await self.mod.nick(ctx, member, name, 'No reason'))[0])

    @commands.command(name='role', description='[Add, Remove] role [to, from] member')
    async def command_role(self, ctx, member: discord.Member, role: discord.Role, *, reason='No reason'):
        '''{prefix}role {mention} {role}'''
        await ctx.reply(embed=(await self.mod.role(ctx, member, role, reason))[0])

    @commands.command(name='slowmode', description='[Change, Remove] channel slowmode')
    @commands.has_permissions(manage_channels=True)
    async def command_slowmode(self, ctx, time: str='0s', *, reason: str='No reason'):
        '''{prefix}slowmode 2m
        {prefix}slowmode 2h Fast Chat'''
        await ctx.reply(embed=(await self.mod.slowmode(ctx, time, reason))[0])

    @slash_command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def slash_kick(self, ctx, member: Option(discord.Member, 'Member you want to kick'), reason: Option(str, 'Reason of the kick', required=False, default='No reason')):
        '''Kick member from the server'''
        await ctx.respond(embed=(temp := (await self.mod.kick(ctx, member, reason)))[0], ephemeral=temp[1])

    @slash_command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def slash_ban(self, ctx, member: Option(discord.Member, 'Member you want to ban'), reason: Option(str, 'Reason of the ban', required=False, default='No reason'), delete_message_days: Option(int, 'The number of days you want the user messages to deleted', required=False, default=0)):
        '''Ban member from the server'''
        await ctx.respond(embed=(temp := (await self.mod.ban(ctx, member, reason, delete_message_days)))[0], ephemeral=temp[1])

    @slash_command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def slash_unban(self, ctx, member: Option(str, '[Id, Name] of the member you want to unban')):
        '''Unban member from the server'''
        await ctx.respond(embed=(temp := (await self.mod.unban(ctx, member)))[0], ephemeral=temp[1])

    @slash_command(name='mute')
    @commands.has_permissions(manage_messages=True)
    async def slash_mute(self, ctx, member: Option(discord.Member, 'Member you want to mute'), time: Option(str, 'Time of the mute', required=False, default='3h'), reason: Option(str, 'The reason of the mute', required=False, default='No reason')):
        '''Mute member (with timeout)'''
        await ctx.respond(embed=(temp := (await self.mod.mute(ctx, member, time, reason)))[0], ephemeral=temp[1])

    @slash_command(name='unmute')
    @commands.has_permissions(manage_messages=True)
    async def slash_unmute(self, ctx, member: Option(discord.Member, 'Member you want to unmute'), reason: Option(str, 'Reason of the unmute', required=False, default='No reason')):
        '''Unmute member (from timout)'''
        await ctx.respond(embed=(temp := (await self.mod.mute(ctx, member, reason=reason, mood=False)))[0], ephemeral=temp[1])

    @slash_command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def slash_lock(self, ctx, channel: Option(discord.TextChannel, 'Channel you want to lock', required=False, default=None)):
        '''Lock a text channel'''
        await ctx.respond(embed=(temp := (await self.mod.lock(ctx, self.lock_check(ctx, channel), 'lock')))[0], ephemeral=temp[1])

    @slash_command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def slash_unlock(self, ctx, channel: Option(discord.TextChannel, 'Channel you want to lock', required=False, default=None)):
        '''Unlock a text channel'''
        await ctx.respond(embed=(temp := (await self.mod.lock(ctx, self.lock_check(ctx, channel), 'unlock')))[0], ephemeral=temp[1])

    @slash_command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def slash_clear(self, ctx, amount: Option(int, 'Amount of messages you want to delete', required=False, default=10), member: Option(discord.Member, 'Member you want to delete their messages', required=False, default=None), role: Option(discord.Role, 'Role you want to delete their users messages', required=False, default=None)):
        '''Delete messages from the channel'''
        await self.mod.clear(ctx, amount, self.clear_check(member, role), True)

    @slash_command(name='nickname')
    async def slash_nick(self, ctx, member: Option(discord.Member, 'Member you want to change his nickname', required=False, default=None), name: Option(str, 'The new nickname', required=False, default=None), reason: Option(str, 'Reason of change the nickname', required=False, default='No reason')):
        '''Change [your, member] nickname'''
        await ctx.respond(embed=(temp := (await self.mod.nick(ctx, (ctx.author if member is None else member), name, reason)))[0], ephemeral=temp[1])

    @slash_command(name='role')
    @commands.has_permissions(manage_roles=True)
    async def slash_role(self, ctx, member: Option(discord.Member, 'Member you want to [add, remove] the role [to, from] it'), role: Option(discord.Role, 'Role you want to give it to that member'), reason: Option(str, 'Reason of [adding, removing] the role', required=False, default='No reason')):
        '''[Add, Remove] role [to, from] a member'''
        await ctx.respond(embed=(temp := (await self.mod.role(ctx, member, role, reason)))[0], ephemeral=temp[1])

    @slash_command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def slash_slowmode(self, ctx, time: Option(str, 'New time you want to change channel slowmode to', required=False, default='0s'), reason: Option(str, 'Reason of change channel slowmode', required=False, default='No reason')):
        '''[Change, Remove] channel slowmode'''
        await ctx.respond(embed=(temp := (await self.mod.slowmode(ctx, time, reason)))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(ModsCommands(bot))
