from graphene_django.views import GraphQLView

from utils.jwt_auth import JSONWebTokenAuthMixin


class StaffGraphQLView(JSONWebTokenAuthMixin, GraphQLView):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            user_role='is_library_staff',
            authorization_error_msg='Only library staff allowed',
            **kwargs
        )
