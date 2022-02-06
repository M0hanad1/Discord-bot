import discord
import topgg
import os
from discord.ext import commands
from dotenv import load_dotenv
from src.prefix.prefix import Prefix


bot = commands.Bot(activity=discord.Game(name='+help'), intents=discord.Intents.all(), command_prefix=Prefix().get_prefix)
bot.topggpy = topgg.DBLClient(bot, os.getenv('TOPGG_TOKEN'), autopost=True, post_shard_count=True)


@bot.event
async def on_ready():
    print(f'{bot.user} is ready')


@bot.event
async def on_autopost_success():
    print(f"Posted server count ({bot.topggpy.guild_count}), shard count ({bot.shard_count})")


for folder in os.listdir('./src'):
    if os.path.exists(os.path.join('src', folder, 'cog.py')):
        bot.load_extension(f'src.{folder}.cog')


if __name__ == '__main__':
    load_dotenv()
    bot.run(os.getenv('TOKEN'))
