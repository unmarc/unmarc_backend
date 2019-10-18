from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied('Unauthorized access')
        return super().dispatch(request, *args, **kwargs)


class IsLibraryStaffMixin(UserPassesTestMixin):
    def handle_no_permission(self):
        raise PermissionDenied('Insufficient permissions')

    def test_func(self):
        return self.request.user.is_library_staff
