from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

    is_library_admin = graphene.Boolean()

    def resolve_is_library_admin(self, info):
        return info.context.user.staff.is_library_admin \
            if info.context.user.is_library_staff else False


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        return user
