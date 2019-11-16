from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene

from users.models import Staff


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'name', 'email', 'is_superuser', 'is_active', 'date_joined', 'staff')
    is_library_staff = graphene.Boolean()


class StaffType(DjangoObjectType):
    class Meta:
        model = Staff
    is_library_admin = graphene.Boolean()


class Query:
    me = graphene.Field(UserType)
    all_users = graphene.List(UserType)
    all_staff = graphene.List(StaffType)

    def resolve_me(self, info):
        return info.context.user

    def resolve_all_users(self, info):
        return get_user_model().objects.select_related('staff').all()

    def resolve_all_staff(self, info):
        return Staff.objects.prefetch_related('user', 'branches').all()
