from .base import *
from .base import env

SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="qWR0mlfB5z8lyP8igGcQZyvALT2Dc0vLIO8SBP3dkgJKrx59pWa20M5LSnHZtWJ4",
)

TEST_RUNNER = "django.test.runner.DiscoverRunner"

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
