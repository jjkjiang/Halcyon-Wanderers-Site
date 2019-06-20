import requests 
import discord
import json
import sys
import asyncio

from django.conf import settings

channelid = int(os.environ['CHANNEL'])
token = os.environ['TOKEN']
event = sys.argv[1]

#Connect to website and pull json for specified event
url = "https://imehi.me/participants/"
data = {'event':event} 
response = requests.post(url = url, data = data)
event_json = json.loads(response.text)

pingList = []
for entry in event_json:
    pingList.append(entry["userid"])

client = discord.Client()

@client.event
async def on_ready():
    guild = await client.fetch_guild(532437793805303808)
    channels = client.get_all_channels()

    #go through all channels the bot has access to, find specified channel
    for channel in channels:
        if channel.id == channelid:
            embed = discord.Embed(title="Tile", description="Desc", color=0xfaa620)
            message = ""
            pingMessage = ""
            for id in pingList:
                user = await guild.fetch_member(id)
                message += user.display_name + '\n'
                pingMessage += user.mention + '\n'
            if message ==  "":
                message = "None"
            embed.add_field(name="Participants:", value=message, inline=False)
            await channel.send(embed=embed)
            temp = await channel.send(pingMessage)
            await temp.delete()
            await sys.exit()
            
client.run(token)
