import json

import requests
from rest_framework.decorators import api_view
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import DiscordID


# Create your views here.


def get_token(code):
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://54.71.46.4/',
        'scope': 'identify'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post("https://discordapp.com/api/v6/oauth2/token", data, headers)

    return response["access_token"]


def update_avatar(id, hash):
    discord_id = DiscordID.objects.get(discord_id=id)
    discord_id.avatar = "https://cdn.discordapp.com/avatars/" + id + "/" + hash


@api_view(['GET'])
def oauth_redirect(request):
    code = request.GET.get('code')
    token = get_token(code)

    headers = {
        'Authorization': token
    }

    response = requests.get("https://discordapp.com/api/v6/users/@me", headers=headers)
    dict = json.loads(response)

    query_results = DiscordID.objects.filter(discord_id=dict['id'])

    if query_results.exists():
        user = query_results.get(discord_id=dict['id']).user
        login(request, user)
        update_avatar(dict['id'], dict['avatar'])
    else:
        user = User.objects.create_user(username=dict['username'])
        DiscordID.objects.create(discord_id=dict['id'], user=user)
        login(request, user)
        update_avatar(dict['id'], dict['avatar'])
