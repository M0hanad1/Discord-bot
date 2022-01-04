import discord
from arabic_reshaper import reshape
from PIL import Image, ImageDraw, ImageFont
from bidi.algorithm import get_display


class Functions:
    @staticmethod
    def create_embeds(ctx, base_embed=('', ''), embed_author=('', ''), embed_footer=None, embed_image='', embed_color=0x000000, embed_field=None):
        new_embed = discord.Embed(
            title=base_embed[0],
            description=base_embed[1],
            color=embed_color
        )

        if embed_footer is None:
            new_embed.set_footer(text=str(ctx.author.name), icon_url=ctx.author.avatar.url)

        new_embed.set_author(name=embed_author[0], icon_url=embed_author[1])
        new_embed.set_image(url=embed_image)

        if embed_field is not None:
            for i in embed_field:
                new_embed.add_field(name=i[0], value=i[1], inline=i[2])

        return new_embed

    @staticmethod
    def create_image(string, path):
        w, h = 450, 150
        img = Image.new('RGB', (w, h), color = 'white')

        fnt = ImageFont.truetype('arial.ttf', 70)
        fw, fh = fnt.getsize(string)
        d = ImageDraw.Draw(img)

        d.text(((w - fw) / 2, (h - fh) / 2), string, font=fnt, fill='black')
        img.save(path)

    @staticmethod
    def arabic_convert(string):
        return get_display(reshape(string))

    @staticmethod
    def temp_check(temp, ctx):
        server_id = ctx.guild.id
        channel_id = ctx.channel.id
        member_id = ctx.author.id

        if server_id not in temp:
            temp[server_id] = {channel_id: [member_id]}
            return False

        else:
            if channel_id not in temp[server_id]:
                temp[server_id][channel_id] = [member_id]
                return False

            if member_id not in temp[server_id][channel_id]:
                temp[server_id][channel_id].append(member_id)
                return False

        return True

    @staticmethod
    def temp_remove(temp, ctx):
        server_id = ctx.guild.id
        channel_id = ctx.channel.id
        member_id = ctx.author.id

        temp[server_id][channel_id].remove(member_id)

        if len(temp[server_id][channel_id]) == 0:
            del temp[server_id][channel_id]

        if len(temp[server_id]) == 0:
            del temp[server_id]
