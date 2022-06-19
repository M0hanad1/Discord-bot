import discord
from discord.ext import commands
from datetime import timedelta
import humanfriendly
from src.moderators.voice import TempVoice
from src.functions.functions import create_embeds, server_avatar
from src.moderators.autorole import AutoRole


class Mods:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.autoroles = AutoRole()
        self.voice = TempVoice()

    @staticmethod
    def role_check(ctx, member: discord.Member):
        if (ctx.author.top_role.position <= member.top_role.position and member.top_role.position != 0 and ctx.guild.owner.id != ctx.author.id) or ctx.guild.owner.id == member.id:
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

        async for i in ctx.guild.bans():
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

        async for i in ctx.guild.bans():
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
        the_mood = [False] if mood == 'lock' else [None, True]

        if perms.send_messages in the_mood:
            return (create_embeds(ctx, (f'{channel.name} channel is already {mood}ed', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

        perms.send_messages = the_mood[0]
        await channel.set_permissions(ctx.guild.default_role, overwrite=perms)

        return (create_embeds(ctx, (f'{channel.name} channel {mood}ed successfully!', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

    async def clear(self, ctx, amount, filter_, mood):
        if amount < 1:
            amount = 1

        elif amount > 100:
            amount = 100

        if mood:
            msg = await ctx.respond(embed=create_embeds(ctx, ('Deleting channel messages...', ''), (ctx.guild.name, server_avatar(ctx.guild))))
            msg = await msg.original_message()

        else:
            msg = await ctx.reply(embed=create_embeds(ctx, ('Deleting channel messages...', ''), (ctx.guild.name, server_avatar(ctx.guild))))
            await ctx.message.delete()

        try:
            if not filter_:
                deleted = await ctx.channel.purge(limit=amount+1, check=lambda x: x.id != msg.id)
                deleted = len(deleted)

            else:
                deleted = 0

                async for i in ctx.channel.history(limit=amount*2):
                        if (filter_[0] == 'member' and filter_[1].id == i.author.id) or (filter_[0] == 'role' and filter_[1] in i.author.roles):
                            await i.delete()
                            deleted += 1

                            if deleted == amount:
                                break

            await msg.delete()

        except:
            pass

        await msg.channel.send(embed=create_embeds(ctx, (f'`{deleted}` messages deleted successfully!', ''), (ctx.guild.name, server_avatar(ctx.guild))), delete_after=8)

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
        return (create_embeds(ctx, ('Nickname changed succussfully', ''), (member.name, member.display_avatar)), False)

    async def role(self, ctx, member: discord.Member, role: discord.Role, reason='No reason'):
        if role.position >= ctx.author.top_role.position and ctx.guild.owner.id != ctx.author.id:
            return (create_embeds(ctx, ('You can\'t change this role', '')), True)

        if role in member.roles:
            await member.remove_roles(role, reason=reason)
            mood = 'removed'

        else:
            await member.add_roles(role, reason=reason)
            mood = 'added'

        return (create_embeds(ctx, (f'Role {mood} successfully\nReason: {reason}', '')), False)

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

    async def temp_voice(self, ctx, voice_channel: discord.VoiceChannel):
        temp_voice_channel = self.voice.get_voice(ctx.guild.id)

        if not voice_channel:
            channel = self.bot.get_channel(temp_voice_channel)

            if not channel:
                if temp_voice_channel:
                    self.voice.remove_voice(ctx.guild.id)

                return (create_embeds(ctx, ('There\'s no temp voice channel on this server', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

            return (create_embeds(ctx, ('', f'**Server temp voice channel: {channel.mention}**'), (ctx.guild.name, server_avatar(ctx.guild))), False)

        if voice_channel.id == temp_voice_channel:
            self.voice.remove_voice(ctx.guild.id)
            return (create_embeds(ctx, ('Temp voice channel `removed` successfully', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

        else:
            self.voice.add_voice(ctx.guild.id, voice_channel.id)
            return (create_embeds(ctx, ('Temp voice channel `added` successfully', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

    async def autorole(self, ctx, role: discord.Role):
        roles = self.autoroles.get_roles(ctx.guild.id)

        for i in roles.copy():
            if not ctx.guild.get_role(i):
                self.autoroles.remove_role(ctx.guild.id, i)
                roles.remove(i)

        if not role:
            if len(roles) == 0:
                return (create_embeds(ctx, ('There\'s no `autoroles` in this server', f'**Use the command: `autorole [role]`\nTo add autorole to the server**'), (ctx.guild.name, server_avatar(ctx.guild))), True)

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

    async def create_temp_channel(self, member: discord.Member, channel: discord.VoiceChannel, mood: bool):
        temp = self.voice.get_voice(member.guild.id)

        if not (temp_channel := self.bot.get_channel(temp)):
            self.voice.remove_voice(member.guild.id)
            return

        if mood and temp == channel.id:
            new_channel = await channel.guild.create_voice_channel(member.name, reason='Temp voice channel', category=channel.category)
            await member.move_to(new_channel, reason='Temp voice channel')
            await new_channel.set_permissions(member, manage_channels=True)
            return

        if not mood and channel in temp_channel.category.voice_channels and channel.id != temp and (not channel.members or len(channel.members) == 0):
            await channel.delete(reason='All members left the temp voice channel')
