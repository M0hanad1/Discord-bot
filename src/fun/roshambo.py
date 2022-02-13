import discord
from discord.ui import View
from discord.ui import Button
from typing import List
from random import choice
from src.functions.functions import create_embeds


class RoshamboButton(Button['Roshambo']):
    emojis = {'Rock': '✊', 'Paper': '✋', 'Scissors': '✌'}

    def __init__(self, item: str):
        super().__init__(label=item, style=discord.ButtonStyle.green, emoji=self.emojis[item])
        self.item = item

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Roshambo = self.view

        if self.item in view.chooses:
            if view.players[1].id == view.bot.user.id:
                items_temp = ['Rock', 'Paper', 'Scissors']
                items_temp.remove(self.item)
                view.chooses[choice(items_temp)] = view.bot.user

            else:
                await interaction.response.edit_message(embed=create_embeds(view.ctx, (f'You all choose `{self.emojis[self.item]}{self.item}`\nNo one won', '')), view=None)
                view.stop()
                return

        view.chooses[self.item] = interaction.user

        if (temp := view.check_winner()):
            emoji1, text1, emoji2, text2 = self.emojis[temp[0]], temp[0], self.emojis[temp[1]], temp[1]
            await interaction.response.edit_message(embed=create_embeds(view.ctx, (f'`{emoji1}{text1}` defeat `{emoji2}{text2}`', f'**{view.chooses[text1].mention} won**'), (view.chooses[text1].name, view.chooses[text1].display_avatar), thumbnail=view.chooses[text1].display_avatar), view=None)
            view.stop()
            return

        view.current_player = view.players[1]
        await interaction.response.edit_message(embed=create_embeds(view.ctx, ('', f'**It\'s now {view.current_player.mention} turn\nChoose one of Rock, Paper and Scissors**'), (view.current_player.name, view.current_player.display_avatar), thumbnail=view.current_player.display_avatar), view=view)


class Roshambo(View):
    children: List[RoshamboButton]

    def __init__(self, ctx, players, mood, bot):
        super().__init__(timeout=120)
        self.ctx = ctx
        self.bot = bot
        self.players = players
        self.current_player = players[0]
        self.chooses = {}
        self.mood = mood

        if players[1].id == bot.user.id:
            self.chooses[choice(['Rock', 'Paper', 'Scissors'])] = bot.user

        for i in ['Rock', 'Paper', 'Scissors']:
            self.add_item(RoshamboButton(i))

    def check_winner(self):
        if 'Rock' in self.chooses and 'Scissors' in self.chooses:
            return ['Rock', 'Scissors']

        elif 'Paper' in self.chooses and 'Rock' in self.chooses:
            return ['Paper', 'Rock']

        elif 'Scissors' in self.chooses and 'Paper' in self.chooses:
            return ['Scissors', 'Paper']

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True

        if self.mood:
            return await self.message.edit_original_message(embed=create_embeds(self.ctx, (f'Time out\nTry to create a new game', '')), view=self)

        return await self.message.edit(embed=create_embeds(self.ctx, (f'Time out\nTry to create a new game', '')), view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user not in self.players:
            await interaction.response.send_message(embed=create_embeds(base_embed=('You can\'t play this game\nCreate your own game', ''), embed_footer=(interaction.user.name, interaction.user.display_avatar)), ephemeral=True)
            return False

        if interaction.user.id != self.current_player.id:
            await interaction.response.send_message(embed=create_embeds(base_embed=('It\'s not your turn', ''), embed_footer=(interaction.user.name, interaction.user.display_avatar)), ephemeral=True)
            return False

        return True
