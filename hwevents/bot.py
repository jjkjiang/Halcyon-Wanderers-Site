import requests 
import discord
import json
import sys
import asyncio

from django.conf import settings

def post_to_channel(id):
    print("hello " + str(id))

def alert(event):
    #Connect to website and pull json for specified event
    url = "https://imehi.me/participants/"
    data = {'event':event} 
    response = requests.post(url = url, data = data)
    event_json = json.loads(response.text)

    pingList = []
    for entry in event_json:
        pingList.append(entry["userid"])

    #get bot token
    token = settings.DISCORD_TOKEN

    #get channel to send message to
    channelid = settings.HW_CHANNEL

    client = discord.Client()

    @client.event
    async def on_ready():
        guild = await client.fetch_guild(532437793805303808)
        channels = client.get_all_channels()

        #go through all channels the bot has access to, find specified channel
        for channel in channels:
            if channel.id == channelid:
                embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
                message = ""
                for id in pingList:
                    user = await guild.fetch_member(id)
                    embed.add_field(name=user.display_name, value=user.mention, inline=True)
                await channel.send(embed=embed)
                await sys.exit()
            
    client.run(token)
