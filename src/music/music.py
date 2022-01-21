import discord
import youtube_dl
import asyncio
from time import gmtime
from requests import get
from discord.ext import commands
from src.functions.functions import *


class Music:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = []
        self.temp = None
        self.vol = 1.0
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    @staticmethod
    def get_time(time):
        if time == 0:
            return 'Live'

        time = gmtime(time)
        result = ''

        if time.tm_hour != 0:
            result += f'{time.tm_hour}:'

        result += f'00:' if time.tm_min == 0 else f'{time.tm_min}:'
        result += f'0{time.tm_sec}' if time.tm_sec < 10 else f'{time.tm_sec}'

        return result

    def start(self, ctx, vc, info):
        vc.play(discord.FFmpegPCMAudio(source=info['formats'][0]['url'], **self.FFMPEG_OPTIONS), after=lambda _=None: self.play_next(ctx))
        vc.source = discord.PCMVolumeTransformer(vc.source, volume=self.vol)

    def play_next(self, ctx):
        vc = ctx.voice_client

        if self.temp is not None and self.temp[-1]:
            self.start(ctx, vc, self.temp[0])
            return

        if len(self.queue) > 0:
            info = self.queue.pop(0)

            self.start(ctx, vc, info)
            self.temp = [info, False]
            asyncio.run_coroutine_threadsafe(ctx.channel.send(embed=create_embeds(ctx, (f'Now playing:', f'**[{info["title"]}]({info["webpage_url"]})**\n**(`{self.get_time(info["duration"])}`)**'), embed_image=info['thumbnail'])), self.bot.loop)
            return

        self.temp = None
        asyncio.run_coroutine_threadsafe(ctx.channel.send(embed=create_embeds(ctx, ('No more songs', '')), delete_after=15), self.bot.loop)

    def check(self, ctx, vc, bot_vc, mood=None):
        if vc is None:
            return [False, create_embeds(ctx, ('Join a voice channel first', ''))]

        if mood == 'join' and bot_vc is not None and len([i for i in bot_vc.channel.members if not i.bot]) > 0:
            return [False, create_embeds(ctx, ('I\'m already in voice channel', ''))]

        if mood is None:
            if bot_vc is None:
                return [False, create_embeds(ctx, ('I\'m not in voice channel', ''))]

            if vc is None or bot_vc.channel.id != vc.channel.id:
                return [False, create_embeds(ctx, ('We must be in the same voice channel', ''))]

        return [True]

    async def join(self, ctx):
        vc = ctx.author.voice

        if not ((temp := self.check(ctx, vc, ctx.guild.me.voice, 'join'))[0]):
            return (temp[1], True)

        try:
            await vc.channel.connect()

        except:
            await ctx.voice_client.move_to(vc.channel)

        return (create_embeds(ctx, ('Bot joined the voice channel', '')), False)

    async def leave(self, ctx):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        await ctx.voice_client.disconnect()
        return (create_embeds(ctx, ('Bot left the voice channel', '')), False)

    async def play(self, ctx, item):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        YDL_OPTIONS = {'format': 'bestaudio/best', "quiet": True}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                if get(item, allow_redirects=False).status_code == 302:
                    raise

                info = ydl.extract_info(item, download=False)

            except:
                try:
                    info = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]

                except:
                    return (create_embeds(ctx, ('I can\'t find this video', '')), True)

            if 'entries' in info:
                return (await self.add_playlist(ctx, vc, info), False)

            if vc.is_playing() or vc.is_paused():
                self.queue.append(info)
                return (create_embeds(ctx, (f'Added to queue:', f'**[{info["title"]}]({info["webpage_url"]})**\n**(`{self.get_time(info["duration"])}`)**'), embed_image=info['thumbnail']), False)

            self.start(ctx, vc, info)
            self.temp = [info, False]
            return (create_embeds(ctx, (f'Now playing:', f'**[{info["title"]}]({info["webpage_url"]})**\n**(`{self.get_time(info["duration"])}`)**'), embed_image=info['thumbnail']), False)

    async def add_playlist(self, ctx, vc, info):
        if vc.is_playing() or vc.is_paused():
            self.queue.append(info['entries'][0])

        [self.queue.append(info['entries'][i]) for i in range(1, len(info['entries']))]
        embed = create_embeds(ctx, (f'Playlist added to queue:', f'**[{info["title"]}]({info["webpage_url"]})**\n**(`{len(info["entries"])}`)**'), embed_image=info['entries'][0]["thumbnail"])

        if not vc.is_playing() and not vc.is_paused():
            self.start(ctx, vc, info['entries'][0])
            self.temp = [info['entries'][0], False]
            embed.add_field(name='Now playing:', value=f'**[{info["entries"][0]["title"]}]({info["entries"][0]["webpage_url"]})**\n**(`{self.get_time(info["entries"][0]["duration"])}`)**')

        return embed

    async def pause(self, ctx):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        vc = ctx.voice_client

        if not vc.is_playing():
            return (create_embeds(ctx, ('Voice isn\'t playing to pause', '')), True)

        vc.pause()
        return (create_embeds(ctx, ('Voice has been paused', '')), False)

    async def resume(self, ctx):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        vc = ctx.voice_client

        if not vc.is_paused():
            return (create_embeds(ctx, ('Voice isn\'t paused to resume', '')), True)

        vc.resume()
        return (create_embeds(ctx, ('Voice has been resumed', '')), False)

    async def stop(self, ctx):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        vc = ctx.voice_client

        if not vc.is_playing() and not vc.is_paused():
            return (create_embeds(ctx, ('There\'s nothing playing to stop', '')), True)

        self.temp = None
        self.queue = []
        vc.stop()
        return (create_embeds(ctx, ('Voice has been stopped', '')), False)

    async def skip(self, ctx):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        vc = ctx.voice_client

        if not vc.is_playing() and not vc.is_paused():
            return (create_embeds(ctx, ('There\'s nothing playing to skip', '')), True)

        self.temp[-1] = False
        vc.stop()

    async def loop(self, ctx):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        vc = ctx.voice_client

        if not vc.is_playing() and not vc.is_paused():
            return (create_embeds(ctx, ('There\'s nothing playing to loop', '')), True)

        self.temp[-1] = True if not self.temp[-1] else False
        temp = 'Looping:' if self.temp[-1] else 'Not looping:'
        return (create_embeds(ctx, (temp, f'**[{self.temp[0]["title"]}]({self.temp[0]["webpage_url"]})**')), False)

    async def queue_display(self, ctx, page):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        if self.temp is None:
            return (create_embeds(ctx, ('There\'s no songs', '')), True)

        message = f'**1:**\n**[{self.temp[0]["title"]}]({self.temp[0]["webpage_url"]})**\n'
        message += '**(`Looping`)**\n\n' if self.temp[-1] else '\n'
        all_messages = []
        num = 1

        for i in self.queue:
            if ((num / 5) - (num // 5)) == 0:
                all_messages.append(message)
                message = ''

            message += f'**{num+1}:**\n**[{i["title"]}]({i["webpage_url"]})**\n\n'
            num += 1

        if len(message) > 0:
            all_messages.append(message)

        page = 1 if (page > len(all_messages) or page < 1) else page

        return (create_embeds(ctx, (f'Queue [{page}/{len(all_messages)}]:', all_messages[page-1])), False)

    async def remove(self, ctx, index):
        if index == 1:
            return (create_embeds(ctx, (f'You already listening to this song', 'Try to use `skip` command')), True)

        if index-1 > len(self.queue) or index < 1:
            return (create_embeds(ctx, (f'There\'s no song with this index in the queue', '')), True)

        temp = self.queue.pop(index-2)['title']
        return (create_embeds(ctx, (f'Song removed successfully from the queue:', f'`{temp}`')), False)

    async def volume(self, ctx, volume):
        if not ((temp := self.check(ctx, ctx.author.voice,  ctx.guild.me.voice))[0]):
            return (temp[1], True)

        vc = ctx.voice_client

        if not vc.is_playing():
            return (create_embeds(ctx, ('There\'s nothing playing to [get | change] the volume', '')), True)

        if volume is None:
            return (create_embeds(ctx, (f'The current volume is: {int(vc.source.volume * 100)}%', '')), False)

        if volume < 0 or volume > 100:
            return (create_embeds(ctx, ('volume must be between 0 and 100', '')), True)

        vc.source.volume = volume / 100
        self.vol = volume / 100
        return (create_embeds(ctx, (f'Volume changed to: {volume}%', '')), False)
