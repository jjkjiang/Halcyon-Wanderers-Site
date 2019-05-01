import json

import requests
from rest_framework.decorators import api_view
from django.http.response import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.models import User

from .models import DiscordID
from django.conf import settings


# Create your views here.


def get_token(code):
    data = {
        'client_id': settings.DISCORD_CLIENT_ID,
        'client_secret': settings.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'https://imehi.me/auth/discord/',
        'scope': 'identify'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post("https://discordapp.com/api/v6/oauth2/token", data, headers)
    response_dict = response.json()

    print(response_dict)

    return response_dict["access_token"]


def update_avatar(id, hash):
    discord_id = DiscordID.objects.get(discord_id=id)
    discord_id.avatar = "https://cdn.discordapp.com/avatars/" + id + "/" + hash
    discord_id.save()


@api_view(['GET'])
def oauth_redirect(request):
    code = request.GET.get('code')
    token = get_token(code)

    headers = {
        'Authorization': "Bearer " + token
    }

    response = requests.get("https://discordapp.com/api/v6/users/@me", headers=headers)
    response_dict = response.json()

    query_results = DiscordID.objects.filter(discord_id=response_dict['id'])

    if query_results.exists():
        user = query_results.get(discord_id=response_dict['id']).user
        login(request, user)
        update_avatar(response_dict['id'], response_dict['avatar'])
    else:
        user = User.objects.create_user(username=response_dict['username'])
        DiscordID.objects.create(discord_id=response_dict['id'], user=user)
        login(request, user)
        update_avatar(response_dict['id'], response_dict['avatar'])

    return HttpResponseRedirect(redirect_to="https://imehi.me")
