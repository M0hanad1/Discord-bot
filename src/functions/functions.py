import discord
import asyncio
from discord.ext import commands
from arabic_reshaper import reshape
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime


def create_embeds(ctx=None, base_embed=('', ''), embed_author=('', ''), embed_footer=None, embed_image='', thumbnail='', embed_color=0x000000, embed_field=None):
    new_embed = discord.Embed(title=base_embed[0], description=base_embed[1], color=embed_color, timestamp=datetime.utcnow())

    if embed_footer is None and ctx is not None:
        new_embed.set_footer(text=f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}', icon_url=member_avatar(ctx.author))

    else:
        new_embed.set_footer(text=embed_footer[0], icon_url=embed_footer[1])

    new_embed.set_author(name=embed_author[0], icon_url=embed_author[1])
    new_embed.set_image(url=embed_image)
    new_embed.set_thumbnail(url=thumbnail)

    if embed_field is not None:
        for i in embed_field:
            new_embed.add_field(name=i[0], value=i[1], inline=i[2])

    return new_embed


def create_image(string, path):
    w, h = 450, 150
    img = Image.new('RGB', (w, h), color = 'white')

    fnt = ImageFont.truetype('./assets/fonts/arial.ttf', 70)
    fw, fh = fnt.getsize(string)
    d = ImageDraw.Draw(img)

    d.text(((w - fw) / 2, (h - fh) / 2), string, font=fnt, fill='black')

    with open(path, 'w'):
        pass

    img.save(path)


def arabic_convert(string):
    return reshape(string)


def temp_check(temp, ctx):
    server_id = ctx.guild.id
    channel_id = ctx.channel.id

    if server_id not in temp:
        temp[server_id] = []

    if channel_id not in temp[server_id]:
        temp[server_id].append(channel_id)
        return False

    return True


def temp_remove(temp, ctx):
    server_id = ctx.guild.id
    channel_id = ctx.channel.id

    temp[server_id].remove(channel_id)

    if len(temp[server_id]) == 0:
        del temp[server_id]


def member_avatar(member: discord.Member):
    try:
        avatar = member.avatar.url

    except:
        avatar = member.default_avatar.url

    return avatar


def server_avatar(server: discord.Guild):
    try:
        icon = server.icon.url

    except:
        icon = ''

    return icon


async def get_member(bot, ctx, member):
    try:
        if member is not None:
            converter = commands.MemberConverter()

            try:
                member = await converter.convert(ctx, member)

            except:
                member = await bot.fetch_user(int(member))

        else:
            member = ctx.author

    except:
        raise commands.MemberNotFound(member)

    return member


async def get_banner(bot, member):
    req = await bot.http.request(discord.http.Route('GET', '/users/{uid}', uid=member.id))
    banner_id = req["banner"]

    if banner_id:
        if banner_id.startswith('a_'):
            return f'https://cdn.discordapp.com/banners/{member.id}/{banner_id}.gif?size=1024'

        return f'https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024'

    return None
