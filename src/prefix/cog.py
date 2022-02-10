from discord.ext import commands
from discord.commands import slash_command, Option
from src.prefix.prefix import Prefix
from src.functions.functions import create_embeds, server_avatar


class PrefixCommands(commands.Cog, name='Prefix'):
    '''Prefix commands'''
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = Prefix()

    def prefix(self, ctx, new_prefix):
        if new_prefix is None:
            return (create_embeds(ctx, (f'The current prefix is: {self.data.prefix(ctx)}', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

        if not ctx.author.guild_permissions.administrator:
            raise commands.MissingPermissions(['Administrator'])

        if len(new_prefix) > 5:
            return (create_embeds(ctx, (f'The prefix length should be less than or equal 5 characters', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

        if new_prefix == '/':
            return (create_embeds(ctx, (f'The prefix can\'t be a slash (/)', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

        prefix = self.data.update_prefix(ctx, new_prefix)

        if prefix is None:
            return (create_embeds(ctx, (f'That\'s the same current prefix', ''), (ctx.guild.name, server_avatar(ctx.guild))), True)

        return (create_embeds(ctx, (f'Prefix changed successfully\nold prefix: {prefix[0]}\nNew prefix: {prefix[1]}', ''), (ctx.guild.name, server_avatar(ctx.guild))), False)

    @commands.command(name='prefix', aliases=['pre'], description='[See, Change] the bot server prefix')
    async def command_prefix(self, ctx, new_prefix: str=None):
        '''{prefix}prefix
        {prefix}prefix {prefix}'''
        await ctx.reply(embed=self.prefix(ctx, new_prefix)[0])

    @slash_command(name='prefix')
    async def slash_prefix(self, ctx, new_prefix: Option(str, 'New prefix you want to have', required=False, default=None)):
        '''[See, Change] the bot server prefix'''
        await ctx.respond(embed=(temp := self.prefix(ctx, new_prefix))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(PrefixCommands(bot))
