from django.core.exceptions import PermissionDenied
from graphene_django.views import GraphQLView

from utils.jwt_auth import JSONWebTokenAuthMixin


class StaffGraphQLView(JSONWebTokenAuthMixin, GraphQLView):
    def check_authorization(self, user):
        if not getattr(user, 'is_library_staff'):
            raise PermissionDenied("Only library staff allowed")
