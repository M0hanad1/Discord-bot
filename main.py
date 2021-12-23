from discord.ext import commands
from random import randint
from os import mkdir
from os.path import exists, isfile
from asyncio import TimeoutError
from json.decoder import JSONDecodeError
import discord
import json


class DiscordBot(commands.Cog):
    user_score = {}
    folder = './data'
    file = '/data.json'
    data_path = folder + file

    if exists(folder) is False:
        mkdir(folder)

        with open(data_path, 'w') as f:
            json.dump({} + '\n', f, indent=4)

    else:
        if isfile(data_path) is False:
            with open(data_path, 'w') as f:
                json.dump({} + '\n', f, indent=4)

    try:
        with open(data_path) as f:
            user_score = json.load(f)

    except JSONDecodeError:
        with open(data_path) as f:
            json.dump({} + '\n', f, indent=4)

    def __init__(self, bot) -> None:
        self.bot = bot

    async def add_score(self, message):
        if str(message.author.id) in DiscordBot.user_score[str(message.guild.id)]:
            DiscordBot.user_score[str(message.guild.id)][str(message.author.id)] += 1

        else:
            DiscordBot.user_score[str(message.guild.id)][str(message.author.id)] = 1

        with open(DiscordBot.data_path, 'w+') as f:
            json.dump(DiscordBot.user_score, f, indent=4)

    async def show_score(self, message, person_id):
        if person_id not in DiscordBot.user_score[str(message.guild.id)]:
            await message.reply(f'<@{person_id}> Score: 0')
            return

        await message.reply(f'<@{person_id}> Score: {DiscordBot.user_score[str(message.guild.id)][person_id]}')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} went online')

    @commands.command()
    async def score(self, ctx, member: discord.Member=None):
        if member is None:
            member = str(ctx.author.id)

        else:
            member = str(member.id)

        if member not in DiscordBot.user_score[str(ctx.guild.id)]:
            await ctx.reply(f'<@{member}> Score: 0')
            return

        await ctx.reply(f'<@{member}> Score: {DiscordBot.user_score[str(ctx.message.guild.id)][member]}')

    @commands.command(aliases=['rand'])
    async def random(self, ctx, start: int = None, end: int = None, user_choice: int = None):
        if user_choice is None:
            if start is not None and end is not None:
                await ctx.reply(f'The Random Number: {randint(start, end)}')
                return

            random_num = randint(1, 10)
            chance = 3

            await ctx.reply(f'Choose a random number from 1 to 10\nYou have 3 chances')

            while True:
                try:
                    message = await self.bot.wait_for('message', check=lambda message: message.content.replace(' ', '').isdigit(), timeout=15.0)

                except TimeoutError:
                    await ctx.send(f'Time out :)\nThe random number: {random_num}')
                    return

                num = int(message.content.replace(' ', ''))

                if num != random_num:
                    chance -= 1

                    if chance == 0:
                        break

                    if num > random_num:
                        await message.reply(f'Wrong\nThe random number is less than {num}\nYou now have {chance} chances')

                    elif num < random_num:
                        await message.reply(f'Wrong\nThe random number is bigger than {num}\nYou now have {chance} chances')

                    continue

                await self.add_score(message)
                await message.reply(f'You won\nYour choice: {num}\nThe random number: {random_num}')
                return

            await message.reply(f'You lose\nThe random number was: {random_num}')
            return

        if user_choice == (random_num := randint(start, end)):
            await ctx.reply(f'You won :D\nYour choice: {user_choice}\nThe random number: {random_num}')
            return

        await ctx.reply(f'You lose :O\nYour choice: {user_choice}\nThe random number: {random_num}')


def setup(bot):
    bot.add_cog(DiscordBot(bot))
