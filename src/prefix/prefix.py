from discord.ext import commands
from src.data.data import Data


class Prefix():
    DEFAULT_PREFIX = '+'

    def __init__(self) -> None:
        self.data = Data()

    def prefix(self, ctx):
        if not self.data.check_server({'_id': ctx.guild.id, 'prefix': {'$exists': True}}):
            return self.DEFAULT_PREFIX

        for i in self.data.get_server({'_id': ctx.guild.id}):
            return i['prefix']

    def get_prefix(self, bot, message):
        if not message.guild:
            return commands.when_mentioned_or(self.DEFAULT_PREFIX)(bot, message)

        return commands.when_mentioned_or(self.prefix(message))(bot, message)

    def update_prefix(self, ctx, new_prefix):
        old_prefix = self.prefix(ctx)

        if old_prefix == new_prefix:
            return None

        if new_prefix == self.DEFAULT_PREFIX:
            self.data.update_server({'_id': ctx.guild.id}, {'$unset': {'prefix': ''}})
            self.data.check_server_len(ctx.guild.id)
            return (old_prefix, self.DEFAULT_PREFIX)

        self.data.update_server({'_id': ctx.guild.id}, {'$set': {'prefix': new_prefix}})
        return (old_prefix, new_prefix)
