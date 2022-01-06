from dotenv import load_dotenv
from discord.ext import commands
import os
import discord


load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot('?', help_command=None, case_insensitive=True, intents=intents)


for folder in os.listdir('./src'):
    if os.path.exists(os.path.join('src', folder, 'cog.py')):
        bot.load_extension(f'src.{folder}.cog')


@bot.event
async def on_ready():
    print(f'{bot.user} is ready')


if __name__ == '__main__':
    bot.run(os.getenv('TOKEN'))
