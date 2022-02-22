import discord
from discord.ext import commands
from src.bot.updates import Updates
from src.functions.functions import create_embeds, server_avatar


class BotInfo:
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.invite_link = 'https://discord.com/api/oauth2/authorize?client_id=895633975274532906&permissions=8&scope=bot%20applications.commands'
        self.top_gg = 'https://top.gg/bot/895633975274532906'
        self.updates_data = Updates()

    async def info(self, ctx):
        developer = await self.bot.fetch_user(self.bot.owner_id)

        try:
            message = f'My prefix in this server is: `{(await self.bot.get_prefix(ctx))[-1]}`, and you '

        except AttributeError:
            message = 'You '

        return create_embeds(
            base_embed=('', f'**I\'m [NGF]({self.invite_link}) a global, moderation, games, fun, music, and custom prefix bot.\nMy developer is someone called [{developer.name}](https://discordapp.com/users/{developer.id})\n{message}can use slash commands: `/`\nYou can [Vote]({self.top_gg}/vote) for on [top.gg]({self.top_gg}) to support me.**'),
            embed_author=(self.bot.user.name, self.bot.user.display_avatar, self.invite_link),
            embed_footer=(f'Developer: {developer.name}#{developer.discriminator}', developer.display_avatar))

    def invite(self, ctx):
        return create_embeds(ctx, ('', f'**That\'s my [Invite]({self.invite_link}) link.\nHope you Enjoy!**'), (self.bot.user.name, self.bot.user.display_avatar, self.invite_link))

    def vote(self, ctx):
        return create_embeds(ctx, ('', f'**That\'s my [Vote]({self.invite_link}) link on [top.gg]({self.top_gg}).\nYour voting means a lot to me.**'), (self.bot.user.name, self.bot.user.display_avatar, self.invite_link))

    async def dev(self, ctx):
        developer = await self.bot.fetch_user(self.bot.owner_id)
        return create_embeds(ctx, ('', f'**The developer is someone called [{developer.name}](https://discordapp.com/users/{developer.id}/).\nHe\'s a programmer who\'s using [Python](https://www.python.org/) language for programming, and he use [Pycord](https://pycord.readthedocs.io/) to create me.**'), (self.bot.user.name, self.bot.user.display_avatar, self.invite_link), (f'Developer: {developer.name}#{developer.discriminator}', developer.display_avatar), embed_field=[(f'{developer.name}#{developer.discriminator}:', 
        '**<:github:944643502162186261> Github | [M0hanad1](https://www.github.com/M0hanad1)\n' +
        f'<:discord:944644804795584582> Discord | [{developer.name}#{developer.discriminator}](https://discordapp.com/users/{developer.id}/)**',
        False)])

    async def updates(self, ctx, channel: discord.TextChannel, message: str):
        server = (ctx.guild.name, server_avatar(ctx.guild))

        if len(data := self.updates_data.get_updates(ctx.guild.id)) > 0 and not self.bot.get_channel(data[0]):
            data = []
            self.updates_data.remove_updates(ctx.guild.id)

        if not any([data, channel, message]):
            try:
                message_ = f'{(await self.bot.get_prefix(ctx.message))[-1]}updates (channel) (message)'

            except AttributeError:
                message_ = '/updates'

            return (create_embeds(ctx, ('There\'s no `updates` channel for bot updates', f'**Use the command: `{message_}`\nTo add updates channel to the server**'), server), True)

        if data and not any([channel, message]):
            return (create_embeds(ctx, ('', '**The `updates` server channel, you\'ll get all the bot updates in this channel**'), server, embed_field=[('Channel:', f'Channel you\'ll get updates in: {self.bot.get_channel(data[0]).mention}', False), ('Message:', 'There\'s no message will send with the bot update message' if len(data) < 2 else f'Message that will send with the bot update message:\n```\n{data[1]}```', False)]), False)

        if (not channel) and message and len(data) == 0:
            return (create_embeds(ctx, ('You must choose a channel for bot updates\nNot just the message', ''), server), True)

        if message and message.lower() != 'none' and not channel:
            self.updates_data.add_message(ctx.guild.id, message)
            return (create_embeds(ctx, ('Message updated seccessfully\nYou will get this message with the update message', ''), server), False)

        if channel and channel.id in data:
            if message and message.lower() != 'none':
                self.updates_data.add_message(ctx.guild.id, message)
                return (create_embeds(ctx, ('Message updated seccessfully\nYou will get this message with the update message', ''), server), False)

            self.updates_data.remove_updates(ctx.guild.id)
            return (create_embeds(ctx, ('Channel removed successfully\nYou now won\'t get any of the bot updates', ''), server), False)

        if len(data) == 2 and message and message.lower() == 'none':
            self.updates_data.remove_message(ctx.guild.id)
            return (create_embeds(ctx, ('Message removed successfully\nThis message won\'t send with the bot update message', ''), server), False)

        self.updates_data.add_channel(ctx.guild.id, channel.id)
        field = [('Channel', channel.mention, False)]

        if message and message.lower() != 'none':
            self.updates_data.add_message(ctx.guild.id, message)
            field.append(('Message:', f'```\n{message}```', False))

        return (create_embeds(ctx, ('', '**You now have bot updates channel**'), server, embed_field=field), False)

    async def send_updates(self, ctx, title, description, fields):
        title = '' if title == '0' else title
        description = '' if description == '0' else description
        fields = eval(fields)
        developer = await self.bot.fetch_user(self.bot.owner_id)
        data = self.updates_data.get_all_updates()
        servers = 0

        for i in data.items():
            guild = await self.bot.fetch_guild(i[0])

            if not guild:
                self.updates_data.remove_server({'_id': i[0]})
                continue

            elif not (channel := self.bot.get_channel(i[1][0])):
                self.updates_data.remove_updates(i[0])
                continue

            try:
                await channel.send(content=i[1][1] if len(i[1]) > 1 else None, embed=create_embeds(base_embed=(title, description), embed_author=(self.bot.user.name, self.bot.user.display_avatar, self.invite_link), embed_footer=(f'Developer: {developer.name}#{developer.discriminator}', developer.display_avatar), embed_field=fields))
                servers += 1

            except:
                pass

        await ctx.reply(embed=create_embeds(ctx, (f'Message send it to `{servers}` servers', '')))
