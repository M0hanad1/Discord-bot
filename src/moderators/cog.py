import discord
from discord.commands import slash_command, Option
from discord.ext import commands
from src.moderators.mods import Mods
from typing import Union
from src.handler.handler import Handler


class ModsCommands(commands.Cog, name='Mods'):
    """Moderations commands"""
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

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def command_kick(self, ctx, member: discord.Member, *, reason='No reason'):
        """To kick member with prefix command"""
        await ctx.reply(embed=(await self.mod.kick(ctx, member, reason))[0])

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def command_ban(self, ctx, member: Union[int, discord.Member], *, reason='No reason'):
        """To ban member with prefix command"""
        await ctx.reply(embed=(await self.mod.ban(ctx, member, reason))[0])

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def command_unban(self, ctx, *, member: str):
        """To unban member with prefix command"""
        await ctx.reply(embed=(await self.mod.unban(ctx, member))[0])

    @commands.command(name='mute')
    @commands.has_permissions(moderate_members=True)
    async def command_mute(self, ctx, member: discord.Member, time='3h', *, reason='No reason'):
        """To mute member with prefix command"""
        await ctx.reply(embed=(await self.mod.mute(ctx, member, time, reason, True))[0])

    @commands.command(name='unmute')
    @commands.has_permissions(moderate_members=True)
    async def command_unmute(self, ctx, member: discord.Member, *, reason='No reason'):
        """To unmute member with prefix command"""
        await ctx.reply(embed=(await self.mod.unmute(ctx, member, reason, False))[0])

    @commands.command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def command_lock(self, ctx, channel: discord.TextChannel=None):
        """To lock a text channel with prefix command"""
        await ctx.reply(embed=(await self.mod.lock(ctx, self.lock_check(ctx, channel), 'lock'))[0])

    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def command_unlock(self, ctx, channel: discord.TextChannel=None):
        """To unlock a text channel with prefix command"""
        await ctx.reply(embed=(await self.mod.lock(ctx, self.lock_check(ctx, channel), 'unlock'))[0])

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def command_clear(self, ctx, amount: int=10):
        """To delete messages from the chat with prefix command"""
        await self.mod.clear(ctx, amount, None, False)

    @commands.command(name='nickname', aliases=['nick'])
    async def command_nick(self, ctx, member: discord.Member, *, name=None):
        """To change member nickname with prefix command"""
        await ctx.reply(embed=(await self.mod.nick(ctx, member, name, 'No reason'))[0])

    @commands.command(name='role')
    async def command_role(self, ctx, member: discord.Member, role: discord.Role, *, reason='No reason'):
        """To [add|remove] role [to|from] member with prefix command"""
        await ctx.reply(embed=(await self.mod.role(ctx, member, role, reason))[0])

    @slash_command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def slash_kick(self, ctx, member: Option(discord.Member, 'Member you want to kick'), reason: Option(str, 'Reason of the kick', required=False, default='No reason')):
        """To kick member with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.kick(ctx, member, reason)))[0], ephemeral=temp[1])

    @slash_command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def slash_ban(self, ctx, member: Option(discord.Member, 'Member you want to ban'), reason: Option(str, 'Reason of the ban', required=False, default='No reason'), delete_message_days: Option(int, 'The number of days you want the user messages to deleted', required=False, default=0)):
        """To ban member with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.ban(ctx, member, reason, delete_message_days)))[0], ephemeral=temp[1])

    @slash_command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def slash_unban(self, ctx, member: Option(str, 'Id/Name of the member you want to unban')):
        """To unban member with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.unban(ctx, member)))[0], ephemeral=temp[1])

    @slash_command(name='mute')
    @commands.has_permissions(manage_messages=True)
    async def slash_mute(self, ctx, member: Option(discord.Member, 'Member you want to mute'), time: Option(str, 'Time of the mute', required=False, default='3h'), reason: Option(str, 'The reason of the mute', required=False, default='No reason')):
        """To timeout member with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.mute(ctx, member, time, reason, True)))[0], ephemeral=temp[1])

    @slash_command(name='unmute')
    @commands.has_permissions(manage_messages=True)
    async def slash_unmute(self, ctx, member: Option(discord.Member, 'Member you want to unmute'), reason: Option(str, 'Reason of the unmute', required=False, default='No reason')):
        """To remove timeout from member with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.unmute(ctx, member, reason, False)))[0], ephemeral=temp[1])

    @slash_command(name='lock')
    @commands.has_permissions(manage_channels=True)
    async def slash_lock(self, ctx, channel: Option(discord.TextChannel, 'Channel you want to lock', required=False, default=None)):
        """To lock a text channel with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.lock(ctx, self.lock_check(ctx, channel), 'lock')))[0], ephemeral=temp[1])

    @slash_command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def slash_unlock(self, ctx, channel: Option(discord.TextChannel, 'Channel you want to lock', required=False, default=None)):
        """To unlock a text channel with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.lock(ctx, self.lock_check(ctx, channel), 'unlock')))[0], ephemeral=temp[1])

    @slash_command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def slash_clear(self, ctx, amount: Option(int, 'Amount of messages you want to delete', required=False, default=10), member: Option(discord.Member, 'The member you want to delete their messages', required=False, default=None), role: Option(discord.Role, 'The role you want to delete their users messages', required=False, default=None)):
        """To delete messages from the chat with slash command"""
        await self.mod.clear(ctx, amount, self.clear_check(member, role), True)

    @slash_command(name='nickname')
    async def slash_nick(self, ctx, member: Option(discord.Member, 'Member you want to change his nickname', required=False, default=None), name: Option(str, 'The new nickname', required=False, default=None), reason: Option(str, 'Reason of change the nickname', required=False, default='No reason')):
        """To change [your | member] nickname with slash command"""
        await ctx.respond(embed=(temp := (await self.mod.nick(ctx, (ctx.author if member is None else member), name, reason)))[0], ephemeral=temp[1])

    @slash_command(name='role')
    @commands.has_permissions(manage_roles=True)
    async def slash_role(self, ctx, member: Option(discord.Member, 'Member you want to [add | remove] the role [to | from] it'), role: Option(discord.Role, 'Role you want to give it to that member'), reason: Option(str, 'Reason of [add | remove] the role', required=False, default='No reason')):
        """To [add | remove] role [to | from] a member"""
        await ctx.respond(embed=(temp := (await self.mod.role(ctx, member, role, reason)))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(ModsCommands(bot))
