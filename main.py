import discord
import json
import random


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        with open('data.json') as f:
            score = json.load(f)

            with open('data.json', 'w') as f:
                json.dump(score, f, indent=4)

        with open('data.json') as f:
            score = json.load(f)

        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.reply('pong')

        if message.content.lower().startswith('random'):
            message_split = message.content.split(' ')

            if len(message_split) <= 2:
                await message.reply('Write all the numbers :(')
                return

            try:
                if int(message_split[1]) == int(message_split[2]) or int(message_split[1]) > int(message_split[2]):
                    await message.reply('**:{**')
                    return
            except ValueError:
                await message.reply('**Really? ._.**')
                return

            num = random.randint(int(message_split[1]), int(message_split[2]))

            if len(message_split) == 3:
                await message.reply(f'The random number: {num}')
                return

            if int(message_split[3]) == num:
                await message.reply(f'You won :D\nYour choice: {message_split[3]}\nThe random number: {num}')

                if str(message.author.id) in score[str(message.guild.id)]:
                    score[str(message.guild.id)][str(message.author.id)] += 1

                else:
                    score[str(message.guild.id)][str(message.author.id)] = 1

                with open('data.json', 'w') as f:
                    json.dump(score, f, indent=4)

            else:
                await message.reply(f'You lose :O\nYour choice: {message_split[3]}\nThe random number: {num}')

        if message.content.lower().startswith('score'):
            if str(message.author.id) not in score[str(message.guild.id)]:
                await message.reply('Your score: 0')
                return

            await message.reply(f'Your score: {score[str(message.guild.id)][str(message.author.id)]}')


client = MyClient()
client.run('ODk1NjMzOTc1Mjc0NTMyOTA2.YV7aIw.yKMuk3-8DPqhcb-EhARQwytDWFE')
