# pylint: skip-file
from .base import *
from .base import env

DEBUG = True

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="usn&hdL^o%AfH462zgFr4EwRMiMdrfcK$N#u55WPQTAgFuTnMDmLvHUtwN74GFj$",
)

ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# django-debug-toolbar - https://django-debug-toolbar.readthedocs.io/en/latest/
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
INTERNAL_IPS = ["127.0.0.1", ]
if env("USE_DOCKER", default="no") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + "1" for ip in ips]


# django-extensions - https://django-extensions.readthedocs.io/en/latest/
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]
