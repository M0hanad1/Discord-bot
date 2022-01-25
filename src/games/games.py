import discord
import time
from random import choice, randint
from discord.ext import commands
from asyncio import TimeoutError
from discord.ui import View
from src.score.score import Score
from src.functions.functions import create_embeds, create_image, arabic_convert, member_avatar


class RandomView(View):
    def __init__(self, ctx, mood):
        super().__init__(timeout=60)
        self.chances = 3
        self.mood = mood
        self.random_number = randint(1, 10)
        self.ctx = ctx
        self.buttons = [i for i in self.children]
        self.value = False

    @discord.ui.button(emoji='1️⃣', custom_id='1', style=discord.ButtonStyle.green)
    async def one_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='2️⃣', custom_id='2', style=discord.ButtonStyle.green)
    async def two_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='3️⃣', custom_id='3', style=discord.ButtonStyle.green)
    async def three_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='4️⃣', custom_id='4', style=discord.ButtonStyle.green)
    async def four_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='5️⃣', custom_id='5', style=discord.ButtonStyle.green)
    async def five_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='6️⃣', custom_id='6', style=discord.ButtonStyle.green)
    async def six_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='7️⃣', custom_id='7', style=discord.ButtonStyle.green)
    async def seven_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='8️⃣', custom_id='8', style=discord.ButtonStyle.green)
    async def eight_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='9️⃣', custom_id='9', style=discord.ButtonStyle.green)
    async def nine_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    @discord.ui.button(emoji='🔟', custom_id='10', style=discord.ButtonStyle.green)
    async def ten_button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.button_callback(button, interaction, int(button.custom_id))

    async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction, id_):
        self.interaction_value = interaction
        message = f'You won!\nYour choice: {id_}\nThe random number: {self.random_number}'

        if id_ == self.random_number:
            await interaction.response.edit_message(embed=create_embeds(self.ctx, (message, '')), view=None)
            self.value = True
            self.stop()
            return

        else:
            self.chances -= 1

            if self.chances == 0:
                await interaction.response.edit_message(embed=create_embeds(self.ctx, (f'You lose!\nThe random number was: {self.random_number}', '')), view=None)
                self.value = False
                self.stop()
                return

            if int(button.custom_id) > self.random_number:
                message = f'Wrong\nThe random number is less than {id_}\nYou have {self.chances} chances'

                for i in range(id_-1, 10):
                    self.remove_item(self.buttons[i])

            else:
                message = f'Wrong\nThe random number is bigger than {id_}\nYou have {self.chances} chances'
                for i in range(0, id_):
                    self.remove_item(self.buttons[i])

            rows = 0
            buttons = self.children.copy()
            self.clear_items()

            for i in range(len(buttons)):
                if i == 5:
                    rows = 1

                buttons[i].row = rows
                self.add_item(buttons[i])

            await interaction.response.edit_message(embed=create_embeds(self.ctx, (message, '')), view=self)

    async def interaction_check(self, interaction: discord.Interaction):
        if self.ctx.author != interaction.user:
            await interaction.response.send_message(embed=create_embeds(self.ctx, (f'You can\'t use this!', ''), embed_footer=(f'{interaction.user.name}#{interaction.user.discriminator}', interaction.user.avatar.url)), ephemeral=True)
            return False

        return True

    async def on_timeout(self) -> None:
        self.value = False

        if self.mood:
            return await self.message.edit_original_message(embed=create_embeds(self.ctx, (f'Time out!\nThe random number was: {self.random_number}', '')), view=None)

        return await self.message.edit(embed=create_embeds(self.ctx, (f'Time out!\nThe random number was: {self.random_number}', '')), view=None)


class Games:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.temp = {}
        self.assets_path = './assets/'
        self.words_path = self.assets_path + 'words/'
        self.img_path = self.assets_path + 'img/'
        self.data = Score(self.bot)

    def temp_check(self, ctx):
        server_id = ctx.guild.id
        channel_id = ctx.channel.id

        if server_id not in self.temp:
            self.temp[server_id] = []

        if channel_id not in self.temp[server_id]:
            self.temp[server_id].append(channel_id)
            return False

        return True

    def temp_remove(self, ctx):
        server_id = ctx.guild.id
        channel_id = ctx.channel.id

        self.temp[server_id].remove(channel_id)

        if len(self.temp[server_id]) == 0:
            del self.temp[server_id]

    async def typing_games(self, ctx, lang, game, mood):
        if self.temp_check(ctx):
            if mood:
                return await ctx.respond(embed=create_embeds(ctx, ('There\'s already a game in this channel', '')), ephemeral=True)

            return await ctx.reply(embed=create_embeds(ctx, ('There\'s already a game in this channel', '')))

        lang = lang.lower()
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
                create_image(arabic_convert(word), self.img_path + 'temp_img.png')

            else:
                create_image(word, self.img_path + 'temp_img.png')

        file, embed = discord.File(f'{self.img_path}temp_img.png', filename='img.png'), create_embeds(ctx, (f'Try to {"write" if game == "fast" else "spell"}:', ''), embed_image='attachment://img.png')

        if mood:
            temp = await ctx.respond(file=file, embed=embed)
            temp = await temp.original_message()

        else:
            temp = await ctx.reply(file=file, embed=embed)

        start = time.time()

        try:
            message = await self.bot.wait_for('message', check= lambda msg: (game == 'fast' and msg.content.lower() == word) or (game == 'spell' and msg.content.lower().strip() == ' '.join([i for i in word])), timeout=6 if game == 'fast' else 8)
            result = str(time.time() - start)[:4]
            await message.add_reaction('<a:yes:931522286383693905>')
            await message.reply(embed=create_embeds(ctx, (f'You Won\nYou took {result}', ''), embed_author=(message.author.name, member_avatar(message.author)), embed_footer=('', '')))
            self.data.upgrade_score(ctx, message.author)

        except TimeoutError:
            embed = create_embeds(ctx, (f'Time out\nNo one get it', ''), embed_footer=('', ''))
            await temp.reply(embed=embed)

        self.temp_remove(ctx)

    async def random(self, ctx, mood):
        view = RandomView(ctx, mood)

        if mood:
            view.message = await ctx.respond(embed=create_embeds(ctx, ('Try to guess the random number!\nYou have 3 chances', '')), view=view)

        else:
            view.message = await ctx.reply(embed=create_embeds(ctx, ('Try to guess the random number!\nYou have 3 chances', '')), view=view)

        await view.wait()

        if view.value:
            self.data.upgrade_score(ctx, ctx.author)

    def roll(self, ctx, min, max):
        if min > max:
            return (create_embeds(ctx, ('The min number should be less than the mex number', '')), True)

        return (create_embeds(ctx, (f'The random number: {randint(min, max)}', '')), False)

    def magic_ball(self, ctx, question):
        responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Don’t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.', 'Yes - definitely.', 'You may rely on it.']
        return create_embeds(ctx, embed_field=[('Question:', f'```\n{question}```', False), ('Answer:', f'```\n{choice(responses)}```', True)])
