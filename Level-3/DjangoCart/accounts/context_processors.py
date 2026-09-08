from django.conf import settings


def authentication_settings(request):
    return {
        "GOOGLE_OAUTH_ENABLED": settings.GOOGLE_OAUTH_ENABLED,
    }
