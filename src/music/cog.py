from discord.ext import commands
from discord.commands import slash_command, Option
from src.music.music import Music
from src.functions.functions import create_embeds


class MusicCommands(commands.Cog, name='Music'):
    '''Music commands'''
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.music = Music(self.bot)

    @commands.command(name='join', description='To join the voice channel', usage='join')
    async def command_join(self, ctx):
        '''{prefix}join'''
        await ctx.reply(embed=(await self.music.join(ctx))[0])

    @commands.command(name='leave', description='Leave the voice channel', usage='leave')
    async def command_leave(self, ctx):
        '''{prefix}leave'''
        await ctx.reply(embed=(await self.music.leave(ctx))[0])

    @commands.command(name='play', description='Play [video, playlist] in voice channel by [name, link]', usage='play [name]')
    async def command_play(self, ctx, *, name):
        '''{prefix}play Celeste Chapter 2 ost
        {prefix}play https://www.youtube.com/watch?v=iik25wqIuFo
        {prefix}play https://youtube.com/playlist?list=PLe1jcCJWvkWiWLp9h3ge0e5v7n6kxEfOG'''
        temp = await ctx.reply(embed=create_embeds(ctx, ('Searching...', '')))
        await temp.edit(embed=(await self.music.play(ctx, name))[0])

    @commands.command(name='pause', description='Pause a voice channel', usage='pause')
    async def command_pause(self, ctx):
        '''{prefix}pause'''
        await ctx.reply(embed=(await self.music.pause(ctx))[0])

    @commands.command(name='resume', description='Resume a voice channel', usage='resume')
    async def command_resume(self, ctx):
        '''{prefix}resume'''
        await ctx.reply(embed=(await self.music.resume(ctx))[0])

    @commands.command(name='stop', description='Stop a voice channel', usage='stop')
    async def command_stop(self, ctx):
        '''{prefix}stop'''
        await ctx.reply(embed=(await self.music.stop(ctx))[0])

    @commands.command(name='skip', description='Skip the current song', usage='skip')
    async def command_skip(self, ctx):
        '''{prefix}skip'''
        temp = await self.music.skip(ctx)

        if temp is not None:
            await ctx.reply(embed=temp[0])

    @commands.command(name='loop', description='Loop on the current song', usage='loop')
    async def command_loop(self, ctx):
        '''{prefix}loop'''
        await ctx.reply(embed=(await self.music.loop(ctx))[0])

    @commands.command(name='queue', description='Show the voice channel queue', usage='page (page=1)')
    async def command_queue(self, ctx, page: int=1):
        '''{prefix}queue
        {prefix}queue 3'''
        await ctx.reply(embed=(await self.music.queue_display(ctx, page))[0])

    @commands.command(name='remove', description='Remove a song from the queue by the index (id)', usage='remove [index]')
    async def command_remove(self, ctx, index: int):
        '''{prefix}remove 2'''
        await ctx.reply(embed=(await self.music.remove(ctx, index))[0])

    @commands.command(name='volume', aliases=['vol'], description='[See, Change] the voice channel volume', usage='volume (volume)')
    async def command_volume(self, ctx, volume: int=None):
        '''{prefix}volume
        {prefix}volume 75'''
        await ctx.reply(embed=(await self.music.volume(ctx, volume))[0])

    @slash_command(name='join')
    async def slash_join(self, ctx):
        '''Join the voice channel'''
        await ctx.respond(embed=(temp := (await self.music.join(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='leave')
    async def slash_leave(self, ctx):
        '''Leave the voice channel'''
        await ctx.respond(embed=(temp := (await self.music.leave(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='play')
    async def slash_play(self, ctx, name: Option(str, '[Name, Link] of the [video, playlist] you want to play')):
        '''Play [video, playlist] in voice channel by [name, link]'''
        await ctx.defer()
        await ctx.respond(embed=(await self.music.play(ctx, name))[0])

    @slash_command(name='pause')
    async def slash_pause(self, ctx):
        '''Pause a voice channel'''
        await ctx.respond(embed=(temp := (await self.music.pause(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='resume')
    async def slash_resume(self, ctx):
        '''Resume a voice channel'''
        await ctx.respond(embed=(temp := (await self.music.resume(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='stop')
    async def slash_stop(self, ctx):
        '''Stop a voice channel'''
        await ctx.respond(embed=(temp := (await self.music.stop(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='skip')
    async def slash_skip(self, ctx):
        '''Skip the current song'''
        temp = await self.music.skip(ctx)

        if temp is not None:
            await ctx.respond(embed=temp[0], ephemeral=temp[1])

        else:
            await ctx.delete()

    @slash_command(name='loop')
    async def slash_loop(self, ctx):
        '''Loop on the current song'''
        await ctx.respond(embed=(temp := (await self.music.loop(ctx)))[0], ephemeral=temp[1])

    @slash_command(name='queue')
    async def slash_queue(self, ctx, page: Option(int, 'Page of the queue you want to see', required=False, default=1)):
        '''Show the voice channel queue'''
        await ctx.respond(embed=(temp := (await self.music.queue_display(ctx, page)))[0], ephemeral=temp[1])

    @slash_command(name='remove')
    async def slash_remove(self, ctx, index: Option(int, 'Index of the song you want to remove')):
        '''Remove a song from the queue by the index (id)'''
        await ctx.respond(embed=(temp := (await self.music.remove(ctx, index)))[0], ephemeral=temp[1])

    @slash_command(name='volume')
    async def slash_volume(self, ctx, volume: Option(int, 'New volume you want to use', required=False, default=None)):
        '''[See, Change] the volume of the voice channel'''
        await ctx.respond(embed=(temp := (await self.music.volume(ctx, volume)))[0], ephemeral=temp[1])


def setup(bot: commands.Bot):
    bot.add_cog(MusicCommands(bot))
