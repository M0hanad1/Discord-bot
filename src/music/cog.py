import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from src.music.music import Music
from src.functions.functions import *


class MusicCommands(commands.Cog, name='Music'):
    """Music commands"""
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music = Music(self.bot)

    @commands.command(name='join')
    async def command_join(self, ctx):
        """To join a voice channel with prefix command"""
        await ctx.reply(embed=(await self.music.join(ctx))[0])

    @commands.command(name='leave')
    async def command_leave(self, ctx):
        """To leave a voice channel with prefix command"""
        await ctx.reply(embed=(await self.music.leave(ctx))[0])

    @commands.command(name='play')
    async def command_play(self, ctx, *, name):
        """To play video in voice channel with prefix command"""
        temp = await ctx.reply(embed=create_embeds(ctx, ('Searching...', '')))
        await temp.edit(embed=(await self.music.play(ctx, name))[0])

    @commands.command(name='pause')
    async def command_pause(self, ctx):
        """To pause a voice channel with prefix command"""
        await ctx.reply(embed=(await self.music.pause(ctx))[0])

    @commands.command(name='resume')
    async def command_resume(self, ctx):
        """To resume a voice channel with prefix command"""
        await ctx.reply(embed=(await self.music.resume(ctx))[0])

    @commands.command(name='stop')
    async def command_stop(self, ctx):
        """To stop a voice channel with prefix command"""
        await ctx.reply(embed=(await self.music.stop(ctx))[0])

    @commands.command(name='skip')
    async def command_skip(self, ctx):
        """To skip current song with prefix command"""
        temp = await self.music.skip(ctx)

        if temp is not None:
            await ctx.reply(embed=temp[0])

    @commands.command(name='loop')
    async def command_loop(self, ctx):
        """To loop in current song with prefix command"""
        await ctx.reply(embed=(await self.music.loop(ctx))[0])

    @commands.command(name='queue')
    async def command_queue(self, ctx, page: int=1):
        """To show voice channel queue with prefix command"""
        await ctx.reply(embed=(await self.music.queue_display(ctx, page))[0])

    @commands.command(name='remove')
    async def command_remove(self, ctx, index: int):
        """To remove song from queue by index (id) with prefix command"""
        await ctx.reply(embed=(await self.music.remove(ctx, index))[0])

    @commands.command(name='volume', aliases=['vol'])
    async def command_volume(self, ctx, volume: int=None):
        """To [see|change] voice channel volume with prefix command"""
        await ctx.reply(embed=(await self.music.volume(ctx, volume))[0])

    @slash_command(name='join')
    async def slash_join(self, ctx):
        """To join a voice channel with slash command"""
        await ctx.respond(embed=(temp := (await self.music.join(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='leave')
    async def slash_leave(self, ctx):
        """To leave a voice channel with slash command"""
        await ctx.respond(embed=(temp := (await self.music.leave(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='play')
    async def slash_play(self, ctx, name: Option(str, '[Name|Link] of the [video|playlist] you want to play')):
        """To play video in voice channel with slash command"""
        await ctx.defer()
        await ctx.respond(embed=(await self.music.play(ctx, name))[0])

    @slash_command(name='pause')
    async def slash_pause(self, ctx):
        """To pause a voice channel with slash command"""
        await ctx.respond(embed=(temp := (await self.music.pause(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='resume')
    async def slash_resume(self, ctx):
        """To resume a voice channel with slash command"""
        await ctx.respond(embed=(temp := (await self.music.resume(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='stop')
    async def slash_stop(self, ctx):
        """To stop a voice channel with slash command"""
        await ctx.respond(embed=(temp := (await self.music.stop(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='skip')
    async def slash_skip(self, ctx):
        """To skip current song with slash command"""
        temp = await self.music.skip(ctx)

        if temp is not None:
            await ctx.respond(embed=temp[0], ephemeral=temp[1])

        else:
            await ctx.delete()

    @slash_command(name='loop')
    async def slash_loop(self, ctx):
        """To loop in current song with slash command"""
        await ctx.respond(embed=(temp := (await self.music.loop(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='queue')
    async def slash_queue(self, ctx, page: Option(int, 'Page of the queue you want to see', required=False, default=1)):
        """To show voice channel queue with slash command"""
        await ctx.respond(embed=(temp := (await self.music.queue_display(ctx, page)))[0], ephemeral=temp[1])

    @slash_command(name='remove')
    async def slash_remove(self, ctx, index: Option(int, 'Index of the song you want to remove')):
        """To remove song from queue by index (id) with slash command"""
        await ctx.respond(embed=(temp := (await self.music.remove(ctx, index)))[0], ephemeral=temp[1])

    @slash_command(name='volume')
    async def slash_volume(self, ctx, volume: Option(int, 'New volume you want to use', required=False, default=None)):
        """To [see|change] voice channel volume with slash command"""
        await ctx.respond(embed=(temp := (await self.music.volume(ctx, volume)))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(MusicCommands(bot))
