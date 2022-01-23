from discord.ext import commands
from src.handler.handler import Handler


class HandlerCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.handler = Handler()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if (temp := self.handler.main(ctx, err)) is not None:
            await ctx.reply(embed=temp)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, err):
        if (temp := self.handler.main(ctx, err)) is not None:
            await ctx.respond(embed=temp, ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(HandlerCommands(bot))
