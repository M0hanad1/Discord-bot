import discord
from discord.ext import commands
from src.functions.functions import Functions


class Mods(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason: str=None):
        if member.id == 589198370111881216:
            await ctx.reply('Go fuck yourself')
            return

        if member == ctx.author:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Error!You can\'t ban yourself', '')))
            return

        # await member.send(embed=Functions.create_embeds(ctx, ('You banned from a server', ''), embed_field=[('From:', ctx.guild.name, False), ('Reason:', reason, False), ('By:', ctx.author.name, False)]))
        await ctx.guild.ban(member, reason=reason)
        await ctx.reply(embed=Functions.create_embeds(ctx, ('Banned from the server', ''), (member.name, member.avatar.url)))

    @commands.command()
    async def unban(self, ctx, member: str):
        try:
            member = await self.bot.fetch_user(int(member))
            member_name, member_disc = member.name, member.discriminator

        except:
            member_name, member_disc = member.split('#')

        for i in await ctx.guild.bans():
            user = i.user

            if (member_name, member_disc) == (user.name, user.discriminator):
                await ctx.guild.unban(user)
                await ctx.reply(embed=Functions.create_embeds(ctx, ('Unbanned from the server', ''), (user.name, user.avatar.url)))
                return

        await ctx.reply(embed=Functions.create_embeds(ctx, ('I can\'t find this member', ''), (member.name, member.avatar.url)))


def setup(bot: commands.Bot):
    bot.add_cog(Mods(bot))

