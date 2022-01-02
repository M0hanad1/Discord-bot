import discord
from discord.ext import commands
from src.functions.functions import Functions
from src.data.data import Data


class MessagesManage(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.data = Data()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is online')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.errors.MissingPermissions):
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Error!\nYou can\'t use this command', '')))

        if isinstance(err, commands.errors.MemberNotFound):
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Error!\nI can\'t find this member', '')))

        print(err)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        temp = self.data.data_search(str(message.guild.id), message.content.lower(), 'server')

        if temp == -1:
            temp = self.data.data_search(str(message.author.id), message.content.lower(), 'user')

            if temp == -1:
                return

        await message.reply(temp)

    async def value_check(self, ctx, value, mood='key'):
        if '<@!' in value and '>' in value:
            if len(value[value.find('<@!')+3:value.find('>')]) == 18:
                await ctx.reply(embed=Functions.create_embeds(ctx, (f'Error!\nThe {mood} can\'t have a member mention!', '')))
                return False

    async def join(self, ctx, mood):
        id_ = str(ctx.guild.id) if mood == 'server' else str(ctx.author.id)

        if self.data.join_data(id_, mood) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Leave the data first', '')))
            return

        await ctx.reply(embed=Functions.create_embeds(ctx, ('Welcome to the data', '')))

    async def leave(self, ctx, mood):
        id_ = str(ctx.guild.id) if mood == 'server' else str(ctx.author.id)

        if self.data.leave_data(id_, mood) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Join the data first', '')))
            return

        await ctx.reply(embed=Functions.create_embeds(ctx, ('You have left the data!', '')))

    async def add(self, ctx, key, value, mood):
        if mood == 'user':
            if await self.value_check(ctx, key) is False or await self.value_check(ctx, value, 'value') is False:
                return

        id_ = str(ctx.guild.id) if mood == 'server' else str(ctx.author.id)

        if (temp := self.data.add_key(id_, key, value, mood)) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Join the data first', '')))
            return

        if temp == -2:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s already a message with this key', '')))
            return

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'The message has been added successfully\nKey: {key}\nValue: {value}', '')))

    async def remove(self, ctx, key, mood):
        id_ = str(ctx.guild.id) if mood == 'server' else str(ctx.author.id)

        if (temp := self.data.remove_key(id_, key, mood)) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Join the data first', '')))
            return

        if temp == -2:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s no message with this key', '')))
            return

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'The message has been deleted successfully', '')))

    async def edit_key(self, ctx, old_key, new_key, mood):
        if mood == 'user' and await self.value_check(ctx, new_key) is False:
            return

        id_ = str(ctx.guild.id) if mood == 'server' else str(ctx.author.id)

        if (temp := self.data.edit_key(id_, old_key, new_key, mood)) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Join the data first', '')))
            return

        if temp == -2:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s no message with this key', '')))
            return

        if temp == -3:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s already a message with this new key', '')))
            return

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'Done\nOld key: {old_key}\nNew key: {new_key}\nValue: {self.data.data_search(id_, new_key, mood)}', '')))

    async def edit_value(self, ctx, key, new_value, mood):
        if mood == 'user' and await self.value_check(ctx, new_value, 'server') is False:
            return

        id_ = str(ctx.guild.id) if mood == 'server' else str(ctx.author.id)
        old_value = self.data.data_search(id_, key, mood)

        if (temp := self.data.edit_value(id_, key, new_value, mood)) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Join the data first', '')))
            return

        if temp == -2:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s no message with this key', '')))
            return

        await ctx.reply(embed=Functions.create_embeds(ctx, (f'Done\nKey: {key}\nOld value: {old_value}\nNew Value: {self.data.data_search(id_, key, mood)}', '')))

    async def show(self, ctx, object, mood):
        id_ = str(object.id)

        try:
            avatar = object.avatar.url if mood == 'user' else object.icon.url

        except AttributeError:
            avatar = ''

        messages = []

        if self.data.data_check(id_, mood) == -1:
            await ctx.reply(embed=Functions.create_embeds(ctx, ('Join the data first', '')))
            return

        if mood == 'user':
            if len(self.data.users_data[id_]['words']) == 0:
                await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s no messages', '')))
                return

            for i in self.data.users_data[id_]['words']:
                messages.append((f'Key: {i}', f'**Value: {self.data.data_search(id_, i, mood)}**', True))

        else:
            if len(self.data.servers_data[id_]['words']) == 0:
                await ctx.reply(embed=Functions.create_embeds(ctx, ('There\'s no messages', '')))
                return

            for i in self.data.servers_data[id_]['words']:
                messages.append((f'Key: {i}', f'**Value: {self.data.data_search(id_, i, mood)}**', True))

        await ctx.reply(embed=Functions.create_embeds(ctx, ('All the keys and values:', ''), (object.name, avatar), embed_field=messages))

    @commands.command(name='show', aliases=['show-u', 'show-l', 'show-user', 'show-local'])
    async def show_local(self, ctx, member: discord.Member=None):
        await self.show(ctx, ctx.author if member is None else member, 'user')

    @commands.command(name='join', aliases=['join-u', 'join-l', 'join-user', 'join-local'])
    async def join_local(self, ctx):
        await self.join(ctx, 'user')

    @commands.command(name='leave', aliases=['leave-u', 'leave-l', 'leave-user', 'leave-local'])
    async def leave_local(self, ctx):
        await self.leave(ctx, 'user')

    @commands.command(name='add', aliases=['add-u', 'add-l', 'add-user', 'add-local'])
    async def add_local(self, ctx, key, *, value):
        await self.add(ctx, key.lower(), value, 'user')

    @commands.command(name='remove', aliases=['remove-u', 'remove-l', 'remove-user', 'remove-local'])
    async def remove_local(self, ctx, *, key):
        await self.remove(ctx, key, 'user')

    @commands.command(name='edit-key', aliases=['edit-key-u', 'edit-key-l', 'edit-key-user', 'edit-key-local'])
    async def edit_key_local(self, ctx, old_key, *, new_key):
        await self.edit_key(ctx, old_key.lower(), new_key.lower(), 'user')

    @commands.command(name='edit-value', aliases=['edit-value-u', 'edit-value-l', 'edit-value-user', 'edit-value-local'])
    async def edit_value_local(self, ctx, old_key, *, new_key):
        await self.edit_value(ctx, old_key.lower(), new_key.lower(), 'user')

    @commands.command(name='show-server', aliases=['show-s', 'show-g', 'show-global'])
    async def show_server(self, ctx):
        await self.show(ctx, ctx.guild, 'server')

    @commands.command(name='join-server', aliases=['join-s', 'join-g', 'join-global'])
    # @commands.has_permissions(manage_messages=True)
    async def join_global(self, ctx):
        await self.join(ctx, 'server')

    @commands.command(name='leave-server', aliases=['leave-s', 'leave-g', 'leave-global'])
    @commands.has_permissions(manage_messages=True)
    async def leave_global(self, ctx):
        await self.leave(ctx, 'server')

    @commands.command(name='add-server', aliases=['add-s', 'add-g', 'add-global'])
    # @commands.has_permissions(manage_messages=True)
    async def add_global(self, ctx, key, *, value):
        await self.add(ctx, key.lower(), value, 'server')

    @commands.command(name='remove-server', aliases=['remove-s', 'remove-g', 'remove-global'])
    # @commands.has_permissions(manage_messages=True)
    async def remove_global(self, ctx, *, key):
        await self.remove(ctx, key.lower(), 'server')

    @commands.command(name='edit-key-server', aliases=['edit-key-s', 'edit-key-g', 'edit-key-global'])
    # @commands.has_permissions(manage_messages=True)
    async def edit_global(self, ctx, old_key, *, new_key):
        await self.edit_key(ctx, old_key.lower(), new_key.lower(), 'server')

    @commands.command(name='edit-value-server', aliases=['edit-value-s', 'edit-value-g', 'edit-value-global'])
    # @commands.has_permissions(manage_messages=True)
    async def edit_value_global(self, ctx, old_key, *, new_key):
        await self.edit_value(ctx, old_key.lower(), new_key.lower(), 'server')


def setup(bot: commands.Bot):
    bot.add_cog(MessagesManage(bot))
