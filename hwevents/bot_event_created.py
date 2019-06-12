import requests 
import discord
import json
import sys
import asyncio

from django.conf import settings

event_id = sys.argv[1]
#event_name = sys.argv[1]
#event_url = sys.argv[2]
#event_desc = sys.argv[3]
#event_image = sys.argv[4]

#Connect to website and pull json for specified event
url = "http://127.0.0.1:8000/event/"
data = {'event':event_id} 
response = requests.post(url = url, data = data)
print(response)
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

#get bot token
token = 'NTc3NTkwNzY3OTc1OTIzNzMz.XNnSCw.NfIFc7LqXdVeVajYLvIxpFcVuCA'#settings.DISCORD_TOKEN

#get channel to send message to
channelid = 577895915319459862 #settings.HW_CHANNEL

client = discord.Client()

@client.event
async def on_ready():
    guild = await client.fetch_guild(532437793805303808)
    channels = client.get_all_channels()

    #go through all channels the bot has access to, find specified channel
    for channel in channels:
        print(channel.name)
        if channel.id == channelid:
            e_title = 'A new event has been posted:'
            e_desc = event_name + '\n' + event_desc + '\n\n' + 'sign up at: ' + event_url
            embed = discord.Embed(title=e_title, description=e_desc, color=0xfaa620)
            embed.set_image(url=event_image)
            await channel.send(embed=embed)
            await sys.exit()
            
client.run(token)
