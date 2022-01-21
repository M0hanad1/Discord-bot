import discord
import os
from discord import commands
from dotenv import load_dotenv
from discord.ext import commands
from src.prefix.prefix import Prefix


load_dotenv()
prefix = Prefix()
bot = commands.Bot(activity=discord.Game(name='/help'), intents=discord.Intents.all(), command_prefix=prefix.get_prefix, case_insensitive=True, owner_id=589198370111881216)


@bot.event
async def on_ready():
    print(f'{bot.user} is ready')


for folder in os.listdir('./src'):
    if os.path.exists(os.path.join('src', folder, 'cog.py')):
        bot.load_extension(f'src.{folder}.cog')

if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
