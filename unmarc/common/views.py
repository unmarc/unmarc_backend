from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_django.views import GraphQLView

from users.mixins import LoginRequiredMixin, IsLibraryStaffMixin


def index(_):
    return HttpResponse('Hello World')


@ensure_csrf_cookie
def set_csrf_cookie(_):
    """
    Call this before any GraphQL queries to set CSRF cookie
    on the browser else all queries will fail
    """
    return HttpResponse()


class PrivateGraphQLView(LoginRequiredMixin, IsLibraryStaffMixin, GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied as e:
            return JsonResponse(
                data={'errors': [{"message": str(e)}]},
                status=403
            )
