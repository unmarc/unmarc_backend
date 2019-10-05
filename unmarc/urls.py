"""unmarc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_django.views import GraphQLView
from .public_schema import schema as public_schema
from .private_schema import schema as private_schema
from common.views import StaffGraphQLView


def index(_):
    return HttpResponse('Hello World')


@ensure_csrf_cookie
def set_csrf_cookie(_):
    """
    Call this before any GraphQL queries to set CSRF cookie
    on the browser else all queries will fail
    """
    return HttpResponse('')


urlpatterns = [
    path('', index),
    path('_h', set_csrf_cookie),
    path('admin/', admin.site.urls),
    path('gql-pub', GraphQLView.as_view(schema=public_schema, graphiql=True)),
    path('gql-pvt', StaffGraphQLView.as_view(schema=private_schema)),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
