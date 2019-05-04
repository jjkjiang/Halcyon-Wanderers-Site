from hwauth.models import DiscordID

def discord_extra_auth(request):
    """
    Similar to django.contrib.auth.context_processors.auth, is addded to include discord id info if needed
    :param request:
    :return:
    """
    if hasattr(request, 'user'):
        try:
            discord = DiscordID.objects.get(user=request.user)

            return {
                'discord': discord,
            }
        except:
            return {}
