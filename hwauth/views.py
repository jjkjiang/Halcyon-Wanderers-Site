import requests
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect

from .models import DiscordID


# Create your views here.


def get_token(code):
    """
    Function that abstracts the process of using the OAuth2 redirected code to retrieve a token for
    identifying the user from Discord
    :param code: OAuth code received from Discord's redirection
    :return: Access token from Discord
    """
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
    """
    Updates DiscordID belonging to a specific user with recent login's avatar URL
    :param id: Discord ID of user
    :param hash: Discord avatar hash of user
    """
    discord_id = DiscordID.objects.get(discord_id=id)
    discord_id.avatar = "https://cdn.discordapp.com/avatars/" + id + "/" + hash
    discord_id.save()


def oauth_redirect(request):
    """
    API view that Discord is redirected to after the user authenticates there that gets an identity token and either
    automatically creates a new user or authenticates the user into their user. Uses Discord ID reported by Discord
    to determine identity.
    :param request: Request data
    :return: Redirect to root
    """
    code = request.GET.get('code')
    token = get_token(code)

    headers = {
        'Authorization': "Bearer " + token
    }

    response = requests.get("https://discordapp.com/api/v6/users/@me", headers=headers)
    response_dict = response.json()

    query_results = DiscordID.objects.filter(discord_id=response_dict['id'])

    user = None

    if query_results.exists():
        user = query_results.get(discord_id=response_dict['id']).user
    else:
        user = User.objects.create_user(username=response_dict['username'])
        DiscordID.objects.create(discord_id=response_dict['id'], user=user)

    login(request, user)
    update_avatar(response_dict['id'], response_dict['avatar'])

    return HttpResponseRedirect(redirect_to="/")


def logout_view(request):
    """
    API view that logs out a user using Django's logout function, which handles all session/cookie work.

    See https://docs.djangoproject.com/en/2.2/topics/auth/default/#how-to-log-a-user-out

    :param request: Request data
    :return: Redirect to root
    """
    logout(request)
    return HttpResponseRedirect(redirect_to="/")
