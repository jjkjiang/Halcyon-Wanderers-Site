from hwauth.models import DiscordID


def discord_extra_auth(request):
    """
    Similar to django.contrib.auth.context_processors.auth

    If the user is authenticated, returns their discordID object to give server side rendering access to fields like
    avatar and ID.
    :param request: Request data
    :return: A discord object if the user is authenticated, or nothing if there is no discordID associated with the user
    (either unauthenticated user or manually created superuser)
    """
    if hasattr(request, 'user'):
        try:
            discord = DiscordID.objects.get(user=request.user)

            return {
                'discord': discord,
            }
        except:
            return {}
