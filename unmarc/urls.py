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
from django.urls import path, include
from graphene_django.views import GraphQLView

from .public_schema import schema as public_schema
from .private_schema import schema as private_schema
from common.views import PrivateGraphQLView, index, set_csrf_cookie
from users import views as users_views


urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('_h/', set_csrf_cookie),
    path('auth-status/', users_views.auth_status),
    path('login/', users_views.login),
    path('logout/', users_views.logout),
    path('gql-pub/', GraphQLView.as_view(schema=public_schema, graphiql=True)),
    path('gql-pvt/', PrivateGraphQLView.as_view(schema=private_schema, graphiql=True)),
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
