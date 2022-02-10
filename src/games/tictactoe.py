import discord
from discord.ui import View
from discord.ui import Button
from typing import List
from src.functions.functions import create_embeds, member_avatar


class TicTacToeButton(Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        if view.board[self.x][self.y] in (view.X, view.O):
            return

        if view.current_player[1] == view.X:
            self.style = discord.ButtonStyle.red
            self.label = 'X'
            view.board[self.x][self.y] = view.X
            view.current_player = [view.player2, view.O]
            embed = create_embeds(view.ctx, ('It\'s now `O`\'s turn', f'**It\'s now {view.player2.mention} turn**'), (view.player2.name, member_avatar(view.player2)), thumbnail=member_avatar(view.player2))

        else:
            self.style = discord.ButtonStyle.green
            self.label = 'O'
            view.board[self.x][self.y] = view.O
            view.current_player = [view.player1, view.X]
            embed = create_embeds(view.ctx, ('It\'s now `X`\'s turn', f'**It\'s now {view.player1.mention} turn**'), (view.player1.name, member_avatar(view.player1)), thumbnail=member_avatar(view.player1))

        if (temp := view.check_winner()) is not None:
            if temp == view.X:
                embed = create_embeds(view.ctx, ('`X` player won', f'**{view.player1.mention} Won**'), (view.player1.name, member_avatar(view.player1)), thumbnail=member_avatar(view.player1))

            elif temp == view.O:
                embed = create_embeds(view.ctx, ('`O` player won', f'**{view.player2.mention} Won**'), (view.player2.name, member_avatar(view.player2)), thumbnail=member_avatar(view.player2))

            else:
                embed = create_embeds(view.ctx, ('It\'s a tie\nNo one won', ''))

            for i in view.children:
                i.disabled = True

            view.stop()

        await interaction.response.edit_message(embed=embed, view=view)


class TicTacToe(View):
    children: List[TicTacToeButton]
    X = -1
    O = 1
    TIE = 2

    def __init__(self, ctx, player1, player2, mood):
        super().__init__(timeout=120)
        self.player1 = player1
        self.player2 = player2
        self.players = [player1, player2]
        self.current_player = [self.player1, self.X]
        self.ctx = ctx
        self.mood = mood
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        for i in range(3):
            for j in range(3):
                self.add_item(TicTacToeButton(j, i))

    def check_values(self, value):
        if value == 3:
            return self.O

        elif value == -3:
            return self.X

    def check_winner(self):
        for i in self.board:
            if (temp := self.check_values(sum(i))):
                return temp

        for i in range(3):
            if (temp := self.check_values(self.board[0][i] + self.board[1][i] + self.board[2][i])):
                return temp

        if (temp := self.check_values(self.board[0][0] + self.board[1][1] + self.board[2][2])):
            return temp

        if (temp := self.check_values(self.board[0][2] + self.board[1][1] + self.board[2][0])):
            return temp

        if all(j != 0 for i in self.board for j in i):
            return self.TIE

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True

        if self.mood:
            return await self.message.edit_original_message(embed=create_embeds(self.ctx, ('Time out\nTry to create a new game', '')), view=self)

        return await self.message.edit(embed=create_embeds(self.ctx, ('Time out\nTry to create a new game', '')), view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user not in self.players:
            await interaction.response.send_message(embed=create_embeds(base_embed=('That\'s not your game\nTry to create your own game', ''), embed_footer=(interaction.user.name, member_avatar(interaction.user))), ephemeral=True)
            return False

        if interaction.user.id != self.current_player[0].id:
            await interaction.response.send_message(embed=create_embeds(base_embed=('It\'s not your turn', ''), embed_footer=(interaction.user.name, member_avatar(interaction.user))), ephemeral=True)
            return False

        return True
