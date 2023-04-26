#main.py
#Counter Strike Rank Updater Bot
import os
import re
import json

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
    user = ctx.message.author
    print(f'{user.name} has called the help command.')

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
    print(f'{user.name} has called the rankup command.')
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

    if(index <= 11):
       await user.add_roles(rankupRole)
       print("added role: " + rankUp)
       await user.remove_roles(currRole)
       print("removed role: " + currRank)
    else:
        await ctx.send(f"Lowest rank achieved.")
        return
    
    embed.set_footer(text=f'{user.display_name} promoted to ' + rankUp)
    file = discord.File(f"../csru/assets/{index+1}.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    await ctx.send(file=file, embed=embed)

@bot.command(pass_context = True)
async def derank(ctx):
    embed = discord.Embed(title='Derank', description='', colour=discord.Colour.blue())

    user = ctx.message.author
    print(f'{user.name} has called the derank command.')
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

    
    if(index >= 0):
       await user.add_roles(deRankRole)
       print(f"added role {deRank}")
       await user.remove_roles(currRole)
       print(f"removed role {deRank}")
    else:
        await ctx.send(f"End of rank range. Nice")
        return

    embed.set_footer(text=f'{user.display_name} demoted to ' + deRank)
    file = discord.File(f"../csru/assets/{index-1}.png", filename="image.png")
    embed.set_image(url="attachment://image.png")
    await ctx.send(file=file, embed=embed)

@bot.command(pass_context=True)
async def rank(ctx, user : discord.Member, role : discord.Role):
    print(f'{user.name} has called the rank command.')

    await user.add_roles(role)
    await ctx.send(f"Set {user.display_name}'s rank to {role.name}")


@bot.command(pass_context=True)
async def update(ctx):
    user = ctx.message.author
    print(f'{user.name} has called the update command.')

    ranksArr = ["Gold Nova 1", "Gold Nova 2", "Gold Nova 3", "Gold Nova Master", "Master Guardian 1", "Master Guardian 2", "Master Guardian Elite", "Distinguished Master Guardian", "Legendary Eagle", "Legendary Eagle Master", "Supreme Master First Class", "Global Elite"]

    

    #open json file of users
    with open("../csru/users/users.json") as f:
        usersData = json.load(f)


    #for loop to loop thru users -> username to match username to message author
    #steam id variable to take in steam id as string to pass into URL

    for i in range(len(usersData['users'])):
        if(user.name == usersData['users'][i]["username"]):
            steamid = usersData['users'][i]['steam_id']


    rankURL = f"https://csgostats.gg/player/{steamid}"
    embed = discord.Embed(title='Update Rank', description='Updating rank...', url=rankURL, colour=discord.Colour.blue())
    embed.set_footer(text=f"{rankURL}")

    await ctx.send(embed = embed)
    f.close()



bot.run(TOKEN)
