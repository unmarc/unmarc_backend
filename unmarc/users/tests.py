from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.test import TestCase

from users.models import User, Staff
from .constants import (
    apps_excluded_from_library_admin_group as excluded_app_labels,
    library_admin_group_name
)


class UserModelTest(TestCase):
    def setUp(self):
        self.regular_user = User.objects.create_user('Rocky Balboa')
        self.staff_user = User.objects.create_user('Frank Slade')
        Staff.objects.create(user=self.staff_user)

    def test_non_staff_user_has_library_staff_property_false(self):
        self.assertFalse(self.regular_user.is_library_staff)

    def test_staff_user_has_library_staff_property_true(self):
        self.assertTrue(self.staff_user.is_library_staff)


class GroupTest(TestCase):
    def test_library_admin_group_exists(self):
        self.assertTrue(Group.objects.filter(name__exact=library_admin_group_name).exists())


class SignalsTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ct_model_prefix = 'dummy_test_model'
        cls.dummy_perm_name = 'Can foo bar'
        cls.perm_codename = 'bar_baz'

        cls.lib_admin_grp = Group.objects.get(name=library_admin_group_name)

        cls.ct = ContentType.objects.create(
            app_label='dummy_test_app',
            model=f'{cls.ct_model_prefix}_x'
        )

        cls.excluded_perms = []

        for num, app_label in enumerate(excluded_app_labels):
            ct = ContentType.objects.create(
                app_label=app_label,
                model=f'{cls.ct_model_prefix}_{num}'
            )
            perm = Permission.objects.create(
                name=cls.dummy_perm_name,
                content_type=ct,
                codename=cls.perm_codename
            )
            cls.excluded_perms.append(perm)

    @classmethod
    def tearDownClass(cls):
        cls.excluded_perms = None
        ContentType.objects.filter(model__startswith=f'{cls.ct_model_prefix}').delete()

    def test_auto_grant_permission_to_library_admin_group_works(self):
        Permission.objects.create(
            name=self.dummy_perm_name,
            content_type=self.ct,
            codename=self.perm_codename
        )
        self.assertTrue(
            self.lib_admin_grp.permissions.filter(
                name=self.dummy_perm_name,
                content_type=self.ct,
                codename__exact=self.perm_codename
            ).exists()
        )

    def test_auto_grant_permission_to_library_admin_group_excludes_excluded_types(self):
        # First verify that newly created permissions from excluded apps exist
        self.assertEqual(len(self.excluded_perms), len(excluded_app_labels))

        # Then verify that none of them are assigned to LibraryAdmin group
        self.assertFalse(
            self.lib_admin_grp.permissions.filter(
                content_type__app_label__in=excluded_app_labels
            ).exists()
        )

    def test_auto_revoke_permission_of_library_admin_group_works(self):
        perm = Permission.objects.create(
            name=self.dummy_perm_name,
            content_type=self.ct,
            codename='baz_foo'
        )
        perm.delete()
        self.assertFalse(
            self.lib_admin_grp.permissions.filter(
                name=self.dummy_perm_name,
                content_type=self.ct,
                codename__exact='baz_foo'
            ).exists()
        )
