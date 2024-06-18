#main.py
#Counter Strike Rank Updater Bot
import os
import re
import json

from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

#load discord token environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#create client instance
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!',intents=intents,activity=discord.Activity(type=discord.ActivityType.watching,name="!h for help"))

#@tasks.loop(minutes=1)
#async def check_stats():
 #   print('Checking stats...')
 

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to the server: {GUILD}')
    print('------------------------------------------------')

@bot.command(pass_context = True)
async def h(ctx):
    user = ctx.message.author
    print(f'{user.name} has called the help command.')

    embed = discord.Embed(title='Help', description='Lists all commands compatible', colour=discord.Colour.blue())
    embed.set_footer(text='!commands : Lists all commands\n'
      '!stats : Gets stats for r6s & updates role in discord Usage: !stats\n')
    await ctx.send(embed=embed)




@bot.command(pass_context=True)
async def stats(ctx):
    user = ctx.message.author
    
    print(f'{user.name} has called the stats command')
    
    #open json file of users
    with open("../csru/users/users.json") as f:
        usersData = json.load(f)
        
    for i in range(len(usersData['users'])):
        if(user.name == usersData['users'][i]["username"]):
            ubisoftID = usersData['users'][i]['ubisoft_id']
    

    rankURL = f'https://r6.tracker.network/r6siege/profile/ubi/{ubisoftID}/overview'
    rankURL_req = requests.get(rankURL)
    
    #find rank through HTML parsing
    rank_soup = BeautifulSoup(rankURL_req.content, 'html.parser')
    rank_body = rank_soup.body
    rank_div = rank_body.find('div', class_='trn-profile-highlighted-content__stats')
    rank_img = rank_div.find('img')
    rank = rank_img.get('alt')
    
    #find KD through HTML parsing
    kd_div = rank_body.find('span', class_='stat-value stat-value--text stat-table__value')
    kd = kd_div.text.strip()
    print(kd)
    
    
    rank_role = discord.utils.get(user.guild.roles, name=rank)

    de_rank_name, rank_up_name = rank_change(rank_role)
    
    de_rank_role = discord.utils.get(user.guild.roles, name=de_rank_name)
    rank_up_role = discord.utils.get(user.guild.roles, name=rank_up_name)
 
    
    await user.remove_roles(de_rank_role)
    await user.remove_roles(rank_up_role)
    await user.add_roles(rank_role)
    

    embed = discord.Embed(title='Rainbow Six Siege Stats', description=f'Stats for {ubisoftID}',url=rankURL,colour=discord.Colour.blue())
    embed.add_field(name="Rank:", value=rank, inline=False)
    file = discord.File(f"../csru/assets/R6S/{rank}.png", filename= "image.png")
    embed.set_thumbnail(url="attachment://image.png")
    
    await ctx.send(file=file, embed=embed)
    

async def rank_change(update_rank):
    with open ("../csru/ranks.txt") as ranks_text:
        rank_arr = ranks_text.readlines()
    
    index = 0;
    
    for i in range(len(rank_arr)):
        if(update_rank == rank_arr[i]):
            index = i;
    
    de_rank = rank_arr[index + 1]
    rank_up = rank_arr[index - 1]
    
    return de_rank, rank_up
    


    

            


bot.run(TOKEN)
