from doctest import Example
import discord
from discord.ui import View, Select
from discord.ext import commands
from discord.commands import SlashCommand
from src.functions.functions import create_embeds
from typing import List
from inspect import Parameter


class HelpSelect(Select['HelpView']):
    def __init__(self, options_, placeholder, mood) -> None:
        options = []
        self.options_ = options_
        self.mood = mood

        for i in options_:
            options.append(discord.SelectOption(label=i[0], description=i[1]))

        super().__init__(placeholder=placeholder, options=options, min_values=1, max_values=1)

        if self.mood == 'bot':
            self.options[0].default = True

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: HelpView = self.view

        for i in self.options:
            if i.default:
                i.default = False

            if i.value == self.values[0]:
                i.default = True

        if self.mood == 'bot':
            cog = self.values[0]

            for i in view.children.copy():
                if i.mood == 'command':
                    view.children.remove(i)

            if cog == 'Main Menu':
                await interaction.response.edit_message(embed=self.options_[0][2], view=view)

            else:
                view.add_item(HelpSelect(view.send_commands(cog), 'Select the command you want to see', 'command'))
                await interaction.response.edit_message(embed=create_embeds(view.ctx, (f'Category: `{cog}`', view.send_cog_help(cog)), (view.bot.user.name, view.bot.user.display_avatar, f'https://top.gg/bot/{view.bot.user.id}')), view=view)

        else:
            await interaction.response.edit_message(embed=await view.send_command_help(self.values[0]), view=view)


class HelpView(View):
    children: List[HelpSelect]

    def __init__(self, bot: commands.Bot, ctx, mood, options):
        super().__init__()
        self.add_item(HelpSelect(options, 'Select the category you want to see.', 'bot'))
        self.ctx = ctx
        self.bot = bot
        self.mood = mood

    def send_cog_help(self, cog):
        cog: commands.Cog = self.bot.get_cog(cog)
        message = ''

        for i in cog.get_commands():
            if isinstance(i, commands.Command) and not self.mood:
                aliases = f'(`{", ".join(i.aliases)}`)' if len(i.aliases) > 0 else ''
                message += f'`{i.name}`{aliases}: {i.description}\n'

            elif isinstance(i, discord.ApplicationCommand) and self.mood:
                message += f'`{i.name}`: {i.description}\n'

        return message

    def send_commands(self, cog):
        cog: commands.Cog = self.bot.get_cog(cog)
        options = []

        for i in cog.get_commands():
            if (isinstance(i, commands.Command) and not self.mood) or (isinstance(i, discord.ApplicationCommand) and self.mood):
                options.append((i.name, i.description))

        return options

    async def send_command_help(self, command):
        if self.mood:
            command = self.bot.get_application_command(command, type=SlashCommand)
            embed = create_embeds(self.ctx, (f'Command: `{command.name}`', command.description), (self.bot.user.name, self.bot.user.display_avatar, f'https://top.gg/bot/{self.bot.user.id}'))

            if len(temp := (command.options)) > 0:
                embed.add_field(name='Options:', value='\n'.join([f'> `{i.name}`: {i.description}' for i in temp]))

        else:
            command = self.bot.get_command(command)
            aliases = f'`{"`, `".join(command.aliases)}`' if len(command.aliases) > 0 else ''
            prefix = (await self.bot.get_prefix(self.ctx.message))[-1]
            embed = create_embeds(self.ctx, (f'Command: `{command.name}`', command.description), (self.bot.user.name, self.bot.user.display_avatar, f'https://top.gg/bot/{self.bot.user.id}'))
            usage = ''

            if len(aliases) > 0:
                embed.add_field(name='Aliases:', value=aliases, inline=False)

            for i, j in command.params.items():
                if i != 'self' and i != 'ctx':
                    usage += f' ({i})' if j.default != Parameter.empty else f' [{i}]'

            embed.add_field(name='Usage:', value=f'`{prefix}{command.name}{usage}`', inline=False)
            embed.add_field(name='Examples:', value=command.help.replace('{prefix}', prefix).replace('{mention}', self.ctx.author.mention).replace('{id}', str(self.ctx.author.id)).replace('{full_name}', f'{self.ctx.author.name}#{self.ctx.author.discriminator}').replace('{text_channel}', self.ctx.channel.mention).replace('{role}', self.ctx.guild.roles[-1].mention), inline=False)

        return embed

    async def on_timeout(self) -> None:
        for i in self.children:
            i.disabled = True

        if self.mood:
            return await self.message.edit_original_message(view=self)

        return await self.message.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(embed=create_embeds(base_embed=('You can\'t use this command\nCreate your own help command', ''), embed_footer=(interaction.user.name, interaction.user.display_avatar)), ephemeral=True)
            return False

        return True


class Help:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_bot_help(self, ctx, mood, mapping):
        options = []
        avatar = self.bot.user.display_avatar
        owner = 'https://discordapp.com/users/589198370111881216/'
        topgg = f'https://top.gg/bot/{self.bot.user.id}'
        embed = create_embeds(ctx, (f'{self.bot.user.name} Help', f'Simple discord bot made by [NOGAF]({owner}).\nThe bot has Moderations, Fun, Music and others commands.\nAnd it has custom prefix feature, score system and more.\nGive it a try.'), (self.bot.user.name, avatar, topgg), thumbnail=avatar, embed_field=[('Links:', f'> **[top.gg]({topgg})**\n> **[Invite](https://discord.com/api/oauth2/authorize?client_id=895633975274532906&permissions=8&scope=bot%20applications.commands)**\n> **[Developer]({owner})**', False)])
        options.append(('Main Menu', 'Bot help main menu', embed))

        for cog in mapping:
            if len(temp := (mapping[cog].get_commands())) != 0 and cog != 'HelpCommand':
                options.append((mapping[cog].__cog_name__, ', '.join([command.name for command in temp if (isinstance(command, commands.Command) and not mood) or (isinstance(command, discord.ApplicationCommand) and mood)])))

        view = HelpView(self.bot, ctx, mood, options)
        view.message = await ctx.respond(embed=embed, view=view) if mood else await ctx.reply(embed=embed, view=view)
