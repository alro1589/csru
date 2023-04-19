#main.py
#Counter Strike Rank Updater Bot
import os
import re

import discord
from discord.ext import commands
from dotenv import load_dotenv

#load discord token environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#create client instance
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to the server: {GUILD}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith("!rankup"):
        await rankup(message.author)


async def rankup(message):
    print("Ranking up...")
    ranks = set(re.findall("gold nova 1|gold nova 2|gold nova 3|gold nova master|master guardian 1|master guardian 2", message.content, re.IGNORECASE))

    if ranks:
        server = bot.get_guild(GUILD)

        roles = [discord.utils.get(server.roles, name=ranks.lower()) for rank in ranks]

        member = await server.fetch_member(message.author.id)

        try:
            await member.add_roles(*roles)
        except Exception as e:
            print(e)
            await message.channel.send("Error.")
        else:
            await message.channel.send("Ranked up.")

bot.run(TOKEN)
