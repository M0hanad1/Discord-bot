import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from src.prefix.prefix import Prefix


load_dotenv()
prefix = Prefix()
bot = commands.Bot(activity=discord.Game(name='+help'), intents=discord.Intents.all(), command_prefix=prefix.get_prefix)


@bot.event
async def on_ready():
    print(f'{bot.user} is ready')


for folder in os.listdir('./src'):
    if os.path.exists(os.path.join('src', folder, 'cog.py')):
        bot.load_extension(f'src.{folder}.cog')

if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
