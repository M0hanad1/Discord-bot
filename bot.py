import discord
import topgg
import os
from discord.ext import commands
from dotenv import load_dotenv
from src.bot.prefix import Prefix
from src.functions.functions import create_embeds


load_dotenv()
bot = commands.Bot(intents=discord.Intents.all(), command_prefix=Prefix().get_prefix, help_command=None, case_insensitive=True, owner_id=589198370111881216)
bot.topggpy = topgg.DBLClient(bot, os.getenv('TOPGG_TOKEN'), autopost=True, post_shard_count=True)


@bot.event
async def on_ready():
    print(f'{bot.user} is ready')

    for i in bot.guilds:
        invite = await i.text_channels[0].create_invite()
        print(i.name, ':', invite)


@bot.event
async def on_autopost_success():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'{bot.topggpy.guild_count} SERVERS'))
    print(f"Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})")


@bot.event
async def on_guild_join(guild: discord.Guild):
    prefix = Prefix.DEFAULT_PREFIX
    developer = await bot.fetch_user(bot.owner_id)
    invite = 'https://discord.com/api/oauth2/authorize?client_id=895633975274532906&permissions=8&scope=bot%20applications.commands'
    top_gg = 'https://top.gg/bot/895633975274532906'
    embed = create_embeds(base_embed=('', f'**Thanks for [Inviting]({invite}) me to your server.\nI\'m [{bot.user.name}]({invite}) a global, moderation, games, fun, music, and custom prefix bot.\nThe developer: [{developer.name}](https://discordapp.com/users/{developer.id}).\nMy default prefix is: `{prefix}`, You can change it with the command: `{prefix}prefix (new_prefix)`.\nTo know all the commands, use `{prefix}help` command.\nIf you want to get all the updates & new features, use the command: `{prefix}updates (channel) (message)`.\nYou can [Vote]({top_gg}/vote) for me on [top.gg]({top_gg}), if you want to support me.**'), embed_author=(bot.user.name, bot.user.display_avatar, invite), embed_footer=(f'Developer: {developer.name}#{developer.discriminator}', developer.display_avatar), thumbnail=bot.user.display_avatar)

    try:
        await guild.public_updates_channel.send(embed=embed)

    except:
        try:
            await guild.system_channel.send(embed=embed)

        except:
            await guild.text_channels[0].send(embed=embed)


for folder in os.listdir('./src'):
    if os.path.exists(os.path.join('src', folder, 'cog.py')):
        bot.load_extension(f'src.{folder}.cog')


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
