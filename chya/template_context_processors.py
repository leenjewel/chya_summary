from django.conf import settings

def common_context_processors(request) :
    return {
        "SITE_TITLE" : settings.SITE_TITLE,
    }

