import discord
from discord.ui import View, Button
from typing import List
from src.functions.functions import create_embeds
from random import randint


class RandomButton(Button['Random']):
    numbers = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

    def __init__(self, number: int):
        super().__init__(style=discord.ButtonStyle.green, emoji=self.numbers[number-1])
        self.number = number

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Random = self.view

        if self.number == view.random_number:
            await interaction.response.edit_message(embed=create_embeds(view.ctx, (f'You won\nYour choice: `{self.number}`\nThe random number: `{view.random_number}`', '')), view=None)
            view.value = True
            view.stop()
            return

        else:
            view.chances -= 1

            if view.chances == 0:
                await interaction.response.edit_message(embed=create_embeds(view.ctx, (f'You lose\nThe random number was: `{view.random_number}`', '')), view=None)
                view.stop()
                return

            if self.number > view.random_number:
                message = f'The random number is less than `{self.number}`\nYou have now `{view.chances}` chances'
                temp = False

                for i in view.children:
                    if i.number == self.number:
                        temp = True

                    if temp:
                        i.disabled = True

            else:
                message = f'The random number is bigger than `{self.number}`\nYou have now `{view.chances}` chances'

                for i in view.children:
                    if i.number > self.number:
                        break

                    i.disabled = True

        await interaction.response.edit_message(embed=create_embeds(view.ctx, (message, '')), view=view)


class Random(View):
    children: List[RandomButton]

    def __init__(self, ctx, mood):
        super().__init__(timeout=120)
        self.random_number = randint(1, 10)
        self.ctx = ctx
        self.value = False
        self.mood = mood
        self.chances = 3

        for i in range(1, 11):
            self.add_item(RandomButton(i))

    async def on_timeout(self) -> None:
        if self.mood:
            return await self.message.edit_original_message(embed=create_embeds(self.ctx, (f'Time out\nThe random number was: `{self.random_number}`', '')), view=None)

        return await self.message.edit(embed=create_embeds(self.ctx, (f'Time out\nThe random number was: `{self.random_number}`', '')), view=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if self.ctx.author.id != interaction.user.id:
            await interaction.response.send_message(embed=create_embeds(base_embed=('You can\'t play this game\nCreate your own game', ''), embed_footer=(interaction.user.name, interaction.user.display_avatar)), ephemeral=True)
            return False

        return True
