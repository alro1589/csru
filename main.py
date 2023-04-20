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
bot = commands.Bot(command_prefix='!', activity=discord.Activity(type=discord.ActivityType.watching, name="!h for help"))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to the server: {GUILD}')

@bot.command(pass_context = True)
async def h(ctx):
    embed = discord.Embed(title='Help', description='Lists all commands compatible', colour=discord.Colour.blue())
    embed.set_footer(text='!commands : Lists all commands\n'
      '!rankup : Changes your role to the next rank\n'
      '!derank : Changes your role to the previous rank\n'
      '!rank : Sets specified users rank to specified rank Usage: !rank @user "rank"\n')
    await ctx.send(embed=embed)


@bot.command(pass_context = True)
@commands.has_role("CSGO")
async def rankup(ctx):
    embed = discord.Embed(title='Rankup', description='', colour=discord.Colour.blue())
    
    user = ctx.message.author
    ranksArr = ["Gold Nova 1", "Gold Nova 2", "Gold Nova 3", "Gold Nova Master", "Master Guardian 1", "Master Guardian 2", "Master Guardian Elite", "Distinguished Master Guardian", "Legendary Eagle", "Legendary Eagle Master", "Supreme Master First Class", "Global Elite"]

    global index
    index = 0

    for i in range(12):
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
    
    embed.set_footer(text=f'{user.display_name} ranked up to ' + rankUp)
    await ctx.send(embed=embed)

@bot.command(pass_context = True)
async def derank(ctx):
    embed = discord.Embed(title='Derank', description='', colour=discord.Colour.blue())

    user = ctx.message.author
    ranksArr = ["Gold Nova 1", "Gold Nova 2", "Gold Nova 3", "Gold Nova Master", "Master Guardian 1", "Master Guardian 2", "Master Guardian Elite", "Distinguished Master Guardian", "Legendary Eagle", "Legendary Eagle Master", "Supreme Master First Class", "Global Elite"]

    global index
    index = 0

    for i in range(12):
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

    embed.set_footer(text=f'{user.display_name} deranked to ' + deRank)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def rank(ctx, user : discord.Member, role : discord.Role):
   await user.add_roles(role)
   await ctx.send(f"Set {user.display_name}'s rank to {role.name}")


bot.run(TOKEN)
