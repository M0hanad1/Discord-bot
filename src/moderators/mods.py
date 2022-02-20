import discord
from discord.ext import commands
from datetime import timedelta
import humanfriendly
from src.functions.functions import create_embeds, server_avatar
from src.moderators.autorole import AutoRole


class Mods:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.temp = 0
        self.autoroles = AutoRole()

    @staticmethod
    def role_check(ctx, member: discord.Member):
        if (ctx.author.top_role.position <= member.top_role.position and member.top_role.position != 0 and ctx.guild.owner.id != ctx.author.id) or ctx.guild.owner.id == member.id:
            return True

        return False

    def clear_check(self, filter, amount, message, msg):
        if filter is None:
            return message.id != msg.id

        if self.temp > amount:
            print(self.temp, amount)
            raise

        if filter[0] == 'member':
            if message.author.id == filter[1].id and message.id != msg.id:
                self.temp += 1
                return True

        elif filter[0] == 'role':
            if filter[1] in message.author.roles and message.id != msg.id:
                self.temp += 1
                return True

        return False

    async def kick(self, ctx, member: discord.Member, reason: str='No reason'):
        if member == ctx.author:
            return (create_embeds(ctx, ('You can\'t kick yourself', '')), True)

        if self.role_check(ctx, member):
            return (create_embeds(ctx, ('You can\'t kick this member', '')), True)

        await ctx.guild.kick(member, reason=reason)
        return (create_embeds(ctx, (f'Kicked from the server\nReason: {reason}', ''), (member.name, member.display_avatar)), False)

    async def ban(self, ctx, member: discord.Member, reason: str='No reason', message_num: int=0):
        try:
            member = await self.bot.fetch_user(int(member))

        except:
            if isinstance(member, int):
                raise commands.MemberNotFound(str(member))

        if member == ctx.author:
            return (create_embeds(ctx, ('You can\'t ban yourself', '')), True)

        for i in await ctx.guild.bans():
            if member == i.user:
                return (create_embeds(ctx, ('You already banned this member', '')), True)

        if member in ctx.guild.members and self.role_check(ctx, member):
            return (create_embeds(ctx, ('You can\'t ban this member', '')), True)

        await ctx.guild.ban(member, reason=reason, delete_message_days=message_num)
        return (create_embeds(ctx, (f'Banned from the server\nReason: {reason}', ''), (member.name, member.display_avatar)), False)

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
                return (create_embeds(ctx, ('Unbanned from the server', ''), (user.name, user.display_avatar)), False)

        raise commands.MemberNotFound(member)

    async def mute(self, ctx, member: discord.Member, time=None, reason='No reason', mood=True):
        if mood:
            if member.timed_out:
                return (create_embeds(ctx, ('This member already muted', '')), True)

            if member == ctx.author:
                return (create_embeds(ctx, ('You can\'t mute yourself', '')), True)

            if self.role_check(ctx, member):
                return (create_embeds(ctx, ('You can\'t mute this member', '')), True)

            if member.guild_permissions.administrator:
                return (create_embeds(ctx, ('You can\'t mute member that has `administrator` permissions', '')), True)

            try:
                time_temp = timedelta(seconds=humanfriendly.parse_timespan(time))

            except:
                return (create_embeds(ctx, ('Unavailable time format', '')), True)

            if time_temp > timedelta(seconds=humanfriendly.parse_timespan('28d')):
                return (create_embeds(ctx, ('Mute time should be less than or equal to `28 day`', '')), True)

            await member.timeout(discord.utils.utcnow() + time_temp)

            return (create_embeds(ctx, (f'Has been muted\nTime: {humanfriendly.format_timespan(time_temp)}\nReason: {reason}', ''), (member.name, member.display_avatar)), False)

        if not member.timed_out:
            return (create_embeds(ctx, ('This member\'s not muted', '')), True)

        await member.remove_timeout(reason=reason)
        return (create_embeds(ctx, (f'Has been unmuted\nReason: {reason}', ''), (member.name, member.display_avatar)), False)

    async def lock(self, ctx, channel, mood):
        perms = channel.overwrites_for(ctx.guild.default_role)
        the_mood = False if mood == 'lock' else None

        if the_mood == perms.send_messages:
            return (create_embeds(ctx, (f'{channel.name} channel is already {mood}ed', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

        perms.send_messages = the_mood
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)

        return (create_embeds(ctx, (f'{channel.name} channel {mood}ed successfully!', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

    async def clear(self, ctx, amount, filter, mood):
        self.temp = 0

        if amount < 1:
            amount = 1

        if amount > 250:
            amount = 250

        if mood:
            msg = await ctx.respond(embed=create_embeds(ctx, ('Deleting channel messages...', ''), (ctx.guild.name, server_avatar(ctx.guild))))
            msg = await msg.original_message()

        else:
            msg = await ctx.reply(embed=create_embeds(ctx, ('Deleting channel messages...', ''), (ctx.guild.name, server_avatar(ctx.guild))))
            await ctx.message.delete()

        if filter is None:
            check = lambda m: self.clear_check(filter, amount, m, msg)

        else:
            the_amount, amount = amount, 999
            check = lambda m: self.clear_check(filter, the_amount, m, msg)

        try:
            deleted = await ctx.channel.purge(limit=amount+1, check=check)
            await msg.delete()

        except:
            print('-')

        await msg.channel.send(embed=create_embeds(ctx, (f'`{len(deleted)}` messages deleted successfully!', ''), (ctx.guild.name, server_avatar(ctx.guild))), delete_after=5)

    async def nick(self, ctx, member: discord.Member, name, reason):
        if member != ctx.author and not ctx.author.guild_permissions.manage_nicknames:
            raise commands.MissingPermissions(['Manage Nicknames'])

        if member == ctx.author and not ctx.author.guild_permissions.change_nickname:
            raise commands.MissingPermissions(['Change Nickname'])

        if member != ctx.author and self.role_check(ctx, member):
            return (create_embeds(ctx, ('You can\'t change this member nickname', '')), True)

        name = member.name if name is None else name

        if len(name) > 32:
            return (create_embeds(ctx, ('The nickname must be `32` ro fewer in length', '')), True)

        old_nick = member.name if member.nick is None else member.nick

        if old_nick == name:
            return (create_embeds(ctx, ('That\'s the same current nickname', ''), (member.name, member.display_avatar)), True)

        await member.edit(nick=name, reason=reason)
        return (create_embeds(ctx, ('Nickname changed succussfully', ''), (member.name, member.display_avatar), embed_field=[('Member:', member.mention, False), ('Old nickname:', old_nick, False), ('New nickname:', name, False), ('Reason:', reason, False)]), False)

    async def role(self, ctx, member: discord.Member, role: discord.Role, reason):
        if role.position >= ctx.author.top_role.position and ctx.guild.owner.id != ctx.author.id:
            return (create_embeds(ctx, ('You can\'t change this role', '')), True)

        if role in member.roles:
            await member.remove_roles(role, reason=reason)
            mood = 'removed'

        else:
            await member.add_roles(role, reason=reason)
            mood = 'added'

        return (create_embeds(ctx, (f'Role {mood} successfully', ''), (member.name, member.display_avatar), embed_field=[('Member:', member.mention, False), ('Role:', role.mention, False), ('Reason', reason, False)]), False)

    async def slowmode(self, ctx, time: str, reason: str):
        try:
            time_temp = humanfriendly.parse_timespan(time)

        except:
            return (create_embeds(ctx, ('Unavailable time format', '')), True)

        if ctx.channel.slowmode_delay == time_temp:
            return (create_embeds(ctx, ('There\'s already a slowmode in this channel with this time' if time_temp != 0 else 'There\'s no slowmode in this channel to remove', '')), True)

        if time_temp > 21600:
            return (create_embeds(ctx, ('New time should be less than or equal to `6 hours`', '')), True)

        await ctx.channel.edit(slowmode_delay=time_temp, reason=reason)

        return (create_embeds(ctx, (f'{ctx.channel.name} slowmode {f"set to `{humanfriendly.format_timespan(time_temp)}`" if time_temp != 0 else "removed successfully"}\nReason: {reason}', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

    async def autorole(self, ctx, role: discord.Role):
        roles = self.autoroles.get_roles(ctx.guild.id)

        for i in roles.copy():
            if not ctx.guild.get_role(i):
                self.autoroles.remove_role(ctx.guild.id, i)
                roles.remove(i)

        if not role:
            if len(roles) == 0:
                return (create_embeds(ctx, ('There\'s no `autoroles` in this server', f'**Use the command: `{(await self.bot.get_prefix(ctx.message))[-1]}autorole [role]`\nTo add autorole to the server**'), (ctx.guild.name, server_avatar(ctx.guild))), True)

            return (create_embeds(ctx, embed_author=(ctx.guild.name, server_avatar(ctx.guild)), embed_field=[('Autoroles:', '**, **'.join([f'<@&{i}>' for i in roles]), False)]), False)

        elif role.id in roles:
            self.autoroles.remove_role(ctx.guild.id, role.id)
            return (create_embeds(ctx, ('', f'**{role.mention} `removed` successfully from the autoroles of this server**'), (ctx.guild.name, server_avatar(ctx.guild))), False)

        else:
            if role.position >= ctx.guild.get_member(self.bot.user.id).top_role.position:
                return (create_embeds(ctx, ('This role is higher than my role\nI can\'t add it', '')), True)

            if len(roles) == 6:
                return (create_embeds(ctx, ('You can just have `6` autoroles', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

            self.autoroles.add_role(ctx.guild.id, role.id)
            return (create_embeds(ctx, ('', f'**{role.mention} `added` successfully to the autoroles of this server**'), (ctx.guild.name, server_avatar(ctx.guild))), False)

    async def add_autoroles(self, member: discord.Member):
        guild: discord.Guild = member.guild
        roles = self.autoroles.get_roles(guild.id)

        for i in roles:
            role = guild.get_role(i)

            if not role:
                self.autoroles.remove_role(guild.id, i)
                continue

            try:
                await member.add_roles(role, reason='Auto Role')

            except:
                pass
