import discord
from discord.ext import commands
import datetime
import humanfriendly
from src.functions.functions import *


class Mods:
    def __init__(self, bot: discord.Bot) -> None:
        self.bot = bot
        self.temp = 0

    def clear_check(self, filter, amount, message, msg):
        if filter is None:
            return message.id != msg.id

        if filter[0] == 'member':
            if message.author.id == filter[1].id and message.id != msg.id and self.temp < amount:
                self.temp += 1
                return True

        elif filter[0] == 'role':
            if filter[1] in message.author.roles and message.id != msg.id and self.temp < amount:
                self.temp += 1
                return True

        return False

    async def kick(self, ctx, member: discord.Member, reason: str='No reason'):
        if member == ctx.author:
            return (create_embeds(ctx, ('Error!\nYou can\'t kick yourself', '')), True)

        await ctx.guild.kick(member, reason=reason)
        return (create_embeds(ctx, (f'Kicked from the server\nReason: {reason}', ''), (member.name, member_avatar(member))), False)

    async def ban(self, ctx, member: discord.Member, reason: str='No reason', message_num: int=0):
        try:
            member = await self.bot.fetch_user(int(member))

        except:
            if type(member) == int:
                raise commands.MemberNotFound(str(member))

        if member == ctx.author:
            return (create_embeds(ctx, ('Error!\nYou can\'t ban yourself', '')), True)

        for i in await ctx.guild.bans():
            if member == i.user:
                return (create_embeds(ctx, ('You already banned this member', '')), True)

        await ctx.guild.ban(member, reason=reason, delete_message_days=message_num)
        return (create_embeds(ctx, (f'Banned from the server\nReason: {reason}', ''), (member.name, member_avatar(member))), False)

    async def unban(self, ctx, member: str):
        try:
            member = await self.bot.fetch_user(int(member))
            member_name, member_disc = member.name, member.discriminator

        except:
            try:
                member_name, member_disc = member.split('#')

            except:
                raise commands.MemberNotFound(member)

        for i in await ctx.guild.bans():
            user = i.user

            if (member_name, member_disc) == (user.name, user.discriminator):
                await ctx.guild.unban(user)
                return (create_embeds(ctx, ('Unbanned from the server', ''), (user.name, member_avatar(user))), False)

        raise commands.MemberNotFound(member)

    async def mute(self, ctx, member: discord.Member, time, reason, mood):
        if mood:
            if member.timed_out:
                return (create_embeds(ctx, ('This member already muted', '')), True)

            if member == ctx.author:
                return (create_embeds(ctx, ('Error!\nYou can\'t mute yourself', '')), True)

            await member.timeout(discord.utils.utcnow() + datetime.timedelta(seconds=humanfriendly.parse_timespan(time)))
            return (create_embeds(ctx, (f'Has been muted\nTime: {time}\nReason: {reason}', ''), (member.name, member_avatar(member))), False)

        if not member.timed_out:
            return (create_embeds(ctx, ('This member\'s not muted', '')), True)

        await member.remove_timeout(reason=reason)
        return (create_embeds(ctx, (f'Has been unmuted\nReason: {reason}', ''), (member.name, member_avatar(member))), False)

    async def lock(self, ctx, channel, mood):
        perms = channel.overwrites_for(ctx.guild.default_role)
        the_mood = False if mood == 'lock' else None

        if the_mood == perms.send_messages:
            return (create_embeds(ctx, (f'{channel.name} channel is already {mood}ed', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

        perms.send_messages = the_mood
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)

        return (create_embeds(ctx, (f'{channel.name} channel {mood}ed successfully!', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

    async def clear(self, ctx, amount, filter, mood):
        if amount < 1:
            amount = 10

        if mood:
            msg = await ctx.respond(embed=create_embeds(ctx, ('Deleting channel messages...', ''), (ctx.guild.name, server_avatar(ctx.guild))))
            msg = await msg.original_message()

        else:
            msg = await ctx.reply(embed=create_embeds(ctx, ('Deleting channel messages...', ''), (ctx.guild.name, server_avatar(ctx.guild))))
            await ctx.message.delete()

        if filter is None:
            check = lambda m: self.clear_check(filter, amount, m, msg)

        else:
            the_amount, amount = amount, 10000000000000
            self.temp = 0
            check = lambda m: self.clear_check(filter, the_amount, m, msg)

        try:
            deleted = await ctx.channel.purge(limit=amount+1, check=check)
            await msg.delete()

        except:
            pass

        await msg.channel.send(embed=create_embeds(ctx, (f'{len(deleted)} messages has been deleted successfully!', ''), (ctx.guild.name, server_avatar(ctx.guild))), delete_after=5)

    async def nick(self, ctx, member: discord.Member, name, reason):
        if member != ctx.author and not ctx.author.guild_permissions.manage_nicknames:
            raise commands.MissingPermissions(['Manage Nicknames'])

        if member == ctx.author and not ctx.author.guild_permissions.change_nickname:
            raise commands.MissingPermissions(['Change Nickname'])

        name = member.name if name is None else name

        if len(name) > 32:
            return (create_embeds(ctx, ('The nick name must be 32 ro fewer in length', '')), True)

        old_nick = member.name if member.nick is None else member.nick

        if old_nick == name:
            return (create_embeds(ctx, ('That\'s the same current nickname', ''), (member.name, member_avatar(member))), True)

        await member.edit(nick=name, reason=reason)
        return (create_embeds(ctx, ('Nickname changed succussfully', ''), (member.name, member_avatar(member)), embed_field=[('Member:', member.mention, False), ('Old nickname:', old_nick, False), ('New nickname:', name, False), ('Reason:', reason, False)]), False)

    async def role(self, ctx, member: discord.Member, role: discord.Role, reason):
        if role in member.roles:
            await member.remove_roles(role, reason=reason)
            mood = 'removed'

        else:
            await member.add_roles(role, reason=reason)
            mood = 'added'

        return (create_embeds(ctx, (f'Role {mood} successfully', ''), (member.name, member_avatar(member)), embed_field=[('Member:', member.mention, False), ('Role:', role.mention, False), ('Reason', reason, False)]), False)
