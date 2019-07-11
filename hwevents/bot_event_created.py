import requests 
import discord
import json
import sys
import asyncio
import os

channelid = int(os.environ['CHANNEL'])
token = os.environ['TOKEN']
event_id = sys.argv[1]

#Connect to website and pull json for specified event
url = "https://imehi.me/event/"
data = {'event':event_id} 
response = requests.post(url = url, data = data)
event_json = json.loads(response.text)

event_name = ""
event_url = ""
event_desc = ""
event_image = ""

for entry in event_json:
    event_name = entry["title"]
    event_url = entry["url"]
    event_desc = entry["description"]
    event_image = entry["image"]

client = discord.Client()

@client.event
async def on_ready():
    guild = await client.fetch_guild(532437793805303808)
    channels = client.get_all_channels()

    #go through all channels the bot has access to, find specified channel
    for channel in channels:
        if channel.id == channelid:
            e_title = 'A new event has been posted:'
            e_desc = event_name + '\n' + event_desc + '\n\n' + 'sign up at: ' + event_url
            embed = discord.Embed(title=e_title, description=e_desc, color=0xfaa620)
            embed.set_image(url=event_image)
            await channel.send(embed=embed)
            await sys.exit()
            
client.run(token)
