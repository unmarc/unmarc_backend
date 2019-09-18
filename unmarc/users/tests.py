from django.test import TestCase

from users.models import User, Staff
from library.models import Branch, Library


class UserModelTest(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user('Rocky Balboa')
        self.staff_user = User.objects.create_user('Frank Slade')
        _library = Library.objects.create(name='Buguri', short_id='buguri')
        _branch = Branch.objects.create(name='JP Nagar', library=_library, short_id='jp-nagar')
        _staff = Staff.objects.create(user=self.staff_user)
        _staff.branches.add(_branch)

    def test_non_staff_user_has_is_library_staff_property_false(self):
        self.assertFalse(self.regular_user.is_library_staff)

    def test_staff_user_has_is_library_staff_property_true(self):
        self.assertTrue(self.staff_user.is_library_staff)
