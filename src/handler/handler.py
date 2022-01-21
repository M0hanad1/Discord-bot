from discord.commands import errors
from discord.ext import commands
from discord.errors import Forbidden
from src.functions.functions import *


class Handler:
    @staticmethod
    def member_missing_permissions(ctx, err):
        return create_embeds(ctx, (f'You must have\n{err.missing_permissions[0].replace("_", " ").title()} permission\nTo use this command', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def bot_missing_permissions(ctx):
        return create_embeds(ctx, ('I can\'t do this command\nCheck my permissions', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def missing_argument(ctx, err):
        return create_embeds(ctx, (f'Missing required argument\n{err.param.name.replace("_", " ").title()} is missing', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def bad_argument(ctx):
        return create_embeds(ctx, ('Bad argument\nTry to use `help` command', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def bad_argument_union(ctx, err):
        return create_embeds(ctx, (f'Bad argument\nOn paramater {err.param.name.replace("_", " ").title()}', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def member_not_found(ctx):
        return create_embeds(ctx, (f'Member not found\nI can\'t find this member', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def channel_not_found(ctx):
        return create_embeds(ctx, (f'Channel not found\nI can\'t find this channel', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    @staticmethod
    def role_not_found(ctx):
        return create_embeds(ctx, (f'Role not found\nI can\'t find this role', ''), (ctx.guild.name, server_avatar(ctx.guild)))

    def main(self, ctx, err):
        if isinstance(err, commands.errors.CommandNotFound):
            return

        elif isinstance(err, (errors.ApplicationCommandInvokeError, commands.errors.CommandInvokeError)):
            return self.main(ctx, err.original)

        elif isinstance(err, commands.MemberNotFound):
            return self.member_not_found(ctx)

        elif isinstance(err, commands.ChannelNotFound):
            return self.channel_not_found(ctx)

        elif isinstance(err, commands.RoleNotFound):
            return self.role_not_found(ctx)

        elif isinstance(err, commands.MissingPermissions):
            return self.member_missing_permissions(ctx, err)

        elif isinstance(err, commands.MissingRequiredArgument):
            return self.missing_argument(ctx, err)

        elif isinstance(err, commands.BadUnionArgument):
            return self.bad_argument_union(ctx, err)

        elif isinstance(err, commands.BadArgument):
            return self.bad_argument(ctx)

        elif isinstance(err, Forbidden):
            return self.bot_missing_permissions(ctx)

        raise err
