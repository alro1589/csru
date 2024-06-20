#main.py
#Counter Strike Rank Updater Bot
import os
import re
import json
import sys

sys.path.append('/Users/Alex/Source/Repos/csru')

import asyncio


from datetime import datetime, timedelta

import discord
from discord.ext import commands
from discord.ext import tasks
from dotenv import load_dotenv

import requests
from bs4 import BeautifulSoup

from music import YTDLSource, ffmpeg_options
from googleapiclient.discovery import build


#load discord token environment
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

YOUTUBE_TOKEN = os.getenv('YOUTUBE_TOKEN')

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


@bot.command(name='stats', help='Fetch R6 Stats')
async def stats(ctx):
    user = ctx.message.author
    
    print(f'{user.name} has called the stats command')
    
    #open json file of users
    with open("../csru/users/users.json") as f:
        usersData = json.load(f)
        
    for i in range(len(usersData['users'])):
        if(user.name == usersData['users'][i]["username"]):
            ubisoftID = usersData['users'][i]['ubisoft_id']
    
    
    rankURL = f'https://r6.tracker.network/r6siege/profile/ubi/{ubisoftID}'
    await refresh_data(f'{rankURL}?forceCollect=true')
    rankURL_req = requests.get(f'{rankURL}/overview')
    
    #find rank through HTML parsing
    rank_soup = BeautifulSoup(rankURL_req.content, 'html.parser')
    rank_body = rank_soup.body
    rank_div = rank_body.find('div', class_='trn-profile-highlighted-content__stats')
    rank_img = rank_div.find('img')
    rank = rank_img.get('alt')
    
    #find KD through HTML parsing
    
    kd, winrate = await grab_stats(rank_soup)
    
    rank_role = discord.utils.get(user.guild.roles, name=rank)

    await rank_change(user, rank)
    await user.add_roles(rank_role)
    

    embed = discord.Embed(title='Rainbow Six Siege Stats', description=f'Stats for {ubisoftID}',url=rankURL,colour=discord.Colour.blue())
    embed.add_field(name="Rank:", value=rank)
    embed.add_field(name="KD:", value=kd)
    embed.add_field(name="Win Rate:", value=f'{winrate}%')
    
    file = discord.File(f"../csru/assets/R6S/{rank}.png", filename= "image.png")
    embed.set_thumbnail(url="attachment://image.png")
    
    await ctx.send(file=file, embed=embed)
    

async def rank_change(user, update_rank):
    with open("../csru/ranks.txt") as ranks_text:
    # Strip newline characters and create a clean list of ranks
        rank_arr = [line.strip() for line in ranks_text.readlines()]

    # Find the index of the current rank in the list
    if update_rank in rank_arr:
        index = rank_arr.index(update_rank)
    
    # Calculate the ranks immediately above and below the current rank, if they exist
    de_rank = rank_arr[index + 1] if index < len(rank_arr) - 1 else None
    rank_up = rank_arr[index - 1] if index > 0 else None
    
    # Remove roles for the ranks immediately above and below, if applicable
    if de_rank:
        de_rank_role = discord.utils.get(user.guild.roles, name=de_rank)
        if de_rank_role:
            await user.remove_roles(de_rank_role)
    if rank_up:
        rank_up_role = discord.utils.get(user.guild.roles, name=rank_up)
        if rank_up_role:
            await user.remove_roles(rank_up_role)
            
    
async def grab_stats(soup):
    kd_ratio = None
    win_rate = None

    # Find all spans for KD ratios and win rates
    stat_spans = soup.find_all('span', class_='stat-value--text')

    for stat_span in stat_spans:
        # Check if the parent or preceding sibling contains specific text to identify the stat
        stat_name_span = stat_span.find_previous_sibling('span', class_='stat-name')
        if stat_name_span:
            stat_name = stat_name_span.text.strip()
            stat_value = stat_span.find('span').text.strip().rstrip('%')  # Remove '%' if present for win rate

            if "KD" in stat_name:  # Adjust this condition based on how KD is labeled
                try:
                    kd_ratio = float(stat_value)
                except ValueError:
                    pass  # Ignore if conversion fails

            elif "Win Rate" in stat_name:
                try:
                    win_rate = float(stat_value)
                except ValueError:
                    pass  # Ignore if conversion fails

    # Return KD ratio and win rate
    return kd_ratio, win_rate
        


async def refresh_data(url):
    response = requests.get(url)
    print(f'Refreshing data for {url}')
    print(response.status_code)
    return response


async def search_song(song_name):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_TOKEN)

    request = youtube.search().list(
        q=song_name,
        part="snippet",
        maxResults=1,
        type="video"
    )
    response = request.execute()

    video_id = response['items'][0]['id']['videoId']
    return f'https://www.youtube.com/watch?v={video_id}'

#music commands
@bot.command(name='play', help='Plays a song')
async def play(ctx, *, song_name:str):
  # Check if the command author is connected to a voice channel
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return

    channel = ctx.author.voice.channel

    # Check if the bot is already connected to a voice channel in the guild
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        # If the bot is not connected, connect to the author's voice channel
        voice_client = await channel.connect()
    elif voice_client.channel != channel:
        # If the bot is connected to a different voice channel, move it to the author's channel
        await voice_client.move_to(channel)

    # Use YTDLSource to fetch the audio source
    url = await search_song(song_name)
    player = await YTDLSource.from_url(url, stream=True)
    ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send(f'Now playing: {player.title}')

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await ctx.author.voice.channel.disconnect()
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
        

@bot.command()
async def play_test(ctx):
    if not ctx.author.voice:
        await ctx.send("You are not connected to a voice channel.")
        return

    channel = ctx.author.voice.channel
    voice_client = await channel.connect()

    source = discord.FFmpegPCMAudio('C:/Users/Alex/source/repos/csru/rockstar.mp3', options=ffmpeg_options)
    voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

bot.run(TOKEN)