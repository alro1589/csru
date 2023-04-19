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

    

@bot.command(pass_context = True)
async def commands(ctx):
   await ctx.send(
      '!commands : Lists all commands\n'
      '!rankup : Changes your role to the next rank\n'
      '!derank : Changes your role to the previous rank\n'
      )


@bot.command(pass_context = True)
async def rankup(ctx):
    user = ctx.message.author
    ranksArr = ["Gold Nova 1", "Gold Nova 2", "Gold Nova 3", "Gold Nova Master", "Master Guardian 1", "Master Guardian 2", "Master Guardian Elite", "Distinguished Master Guardian"]

    global index
    index = 0

    for i in range(8):
        if(ranksArr[i] == ranksArr[i] in [y.name for y in user.roles]):
           index = i


    
    currRank = ranksArr[index]
    currRole = discord.utils.get(user.guild.roles, name=currRank)
    rankUp = ranksArr[index + 1]
    rankupRole = discord.utils.get(user.guild.roles, name=rankUp)

    if(rankupRole in user.roles):
       rankUp = ranksArr[index + 1]
       rankupRole = discord.utils.get(user.guild.roles, name=rankUp)
       await user.add_roles(rankupRole)
       print("added role: " + rankUp)
       await user.remove_roles(currRole)
       print("removed role: " + currRank)
    else:
       await user.add_roles(rankupRole)
       await user.remove_roles(currRole)
    
    await ctx.send('Ranked up to ' + rankUp)

@bot.command(pass_context = True)
async def derank(ctx):
    user = ctx.message.author
    ranksArr = ["Gold Nova 1", "Gold Nova 2", "Gold Nova 3", "Gold Nova Master", "Master Guardian 1", "Master Guardian 2", "Master Guardian Elite", "Distinguished Master Guardian"]

    global index
    index = 0

    for i in range(8):
        if(ranksArr[i] == ranksArr[i] in [y.name for y in user.roles]):
           index = i


    
    currRank = ranksArr[index]
    currRole = discord.utils.get(user.guild.roles, name=currRank)
    deRank = ranksArr[index - 1]
    deRankRole = discord.utils.get(user.guild.roles, name=deRank)

    if(deRankRole in user.roles):
       deRank = ranksArr[index - 1]
       deRankRole = discord.utils.get(user.guild.roles, name=deRank)
       await user.add_roles(deRankRole)
       print("added role: " + deRank)
       await user.remove_roles(currRole)
       print("removed role: " + currRank)
    else:
       await user.add_roles(deRankRole)
       await user.remove_roles(currRole)
    
    await ctx.send('Deranked to ' + deRank)


bot.run(TOKEN)
