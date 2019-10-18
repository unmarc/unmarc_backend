from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from graphene_django.views import GraphQLView

from users.mixins import LoginRequiredMixin, IsLibraryStaffMixin


class StaffGraphQLView(LoginRequiredMixin, IsLibraryStaffMixin, GraphQLView):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied as e:
            return JsonResponse(
                data={'errors': [{"message": str(e)}]},
                status=403
            )
