import discord
import time
from src.functions.functions import Functions
from src.score.score import ScoreData
from random import choice, randint
from discord.ext import commands
from asyncio import TimeoutError


class Games(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.temp = {}
        self.assest_path = './assest/'
        self.words_path = self.assest_path + 'words/'
        self.img_path = self.assest_path + 'img/'
        self.data = ScoreData()

    async def typing_games(self, ctx, lang, mood):
        if Functions.temp_check(self.temp, ctx):
            await ctx.reply(embed=Functions.create_embeds(ctx, ('You already in a game', '')))
            return

        lang_files = [f'{self.words_path}english_words.txt', f'{self.words_path}arabic_words.txt']

        if lang == 'en' or lang == 'english':
            the_lang = lang_files[0]

        elif lang == 'ar' or lang == 'arabic':
            the_lang = lang_files[1]

        else:
            the_lang = choice(lang_files)

        with open(the_lang, encoding='utf-8') as f:
            word = choice(f.readlines()).replace('\n', '')

            if the_lang == lang_files[1]:
                Functions.create_image(Functions.arabic_convert(word), self.img_path + 'temp_img.png')

            else:
                Functions.create_image(word, self.img_path + 'temp_img.png')

        await ctx.reply(
            file=discord.File(f'{self.img_path}temp_img.png', filename='img.png'),
            embed=Functions.create_embeds(ctx, embed_image='attachment://img.png')
            )

        start = time.time()
        result = str(time.time() - start)
        loop_con = 6 if mood == 'fast' else 8

        while float(result[:4]) < loop_con:
            try:
                message = await self.bot.wait_for('message', check=lambda message: ctx.author == message.author, timeout=0.01)

            except TimeoutError:
                result = str(time.time() - start)
                continue

            if (mood == 'fast' and message.content.lower() == word) or (mood == 'dis' and message.content.lower() == ' '.join([i for i in word])):
                self.data.add_score(message.author.id, self.data.get_score(message.author.id) + 1)
                await message.reply(embed=Functions.create_embeds(ctx, (f'You Won\nYou took {result[:4]}', '')))
                Functions.temp_remove(self.temp, ctx)
                return

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'You lose\nYou took {result[:4]} Second', '')))
        Functions.temp_remove(self.temp, ctx)

    @commands.command(aliases=['fast'])
    async def speed(self, ctx, lang=None):
        await self.typing_games(ctx, lang, 'fast')

    @commands.command(aliases=['disassemble'])
    async def dis(self, ctx, lang=None):
        await self.typing_games(ctx, lang, 'dis')

    @commands.command(aliases=['rand'])
    async def random(self, ctx):
        if Functions.temp_check(self.temp, ctx):
            await ctx.reply(embed=Functions.create_embeds(ctx, ('You already in a game', '')))
            return

        random_num = randint(1, 10)
        chance = 3

        await ctx.reply(embed=Functions.create_embeds(ctx, ('Choose a random number from 1 to 10\nYou have 3 chances', '')))

        while True:
            try:
                message = await self.bot.wait_for('message', check=lambda message: message.content.isdigit() and ctx.author == message.author, timeout=15.0)

            except TimeoutError:
                await ctx.reply(embed=Functions.create_embeds(ctx, (f'Time out\nThe random number was: {random_num}', '')))
                Functions.temp_remove(self.temp, ctx)
                return

            num = int(message.content)

            if num != random_num:
                chance -= 1

                if chance == 0:
                    break

                if num > random_num:
                    await message.reply(embed=Functions.create_embeds(message, (f'Wrong\nThe random number is less than {num}\nYou now have {chance} chances', '')))

                elif num < random_num:
                    await message.reply(embed=Functions.create_embeds(message, (f'Wrong\nThe random number is bigger than {num}\nYou now have {chance} chances', '')))

                continue

            self.data.add_score(message.author.id, self.data.get_score(message.author.id) + 1)
            await message.reply(embed=Functions.create_embeds(message, (f'You Won\nThe random number was: {random_num}', '')))
            Functions.temp_remove(self.temp, ctx)
            return

        await message.reply(embed=Functions.create_embeds(message, (f'You lose\nThe random number was: {random_num}', '')))
        Functions.temp_remove(self.temp, ctx)
        return

def setup(bot: commands.Bot):
    bot.add_cog(Games(bot))
