from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .constants import (
    apps_excluded_from_library_admin_group as excluded_app_labels,
    library_admin_group_name
)


def _get_types_and_group():
    return (
        ContentType.objects.filter(app_label__in=excluded_app_labels),
        Group.objects.get(name__exact=library_admin_group_name)
    )


@receiver(post_save, sender=Permission)
def auto_grant_permission_to_library_admin_group(sender, instance, created, **kwargs):
    excluded_content_types, library_admin_group = _get_types_and_group()

    if created and instance.content_type not in excluded_content_types:
        library_admin_group.permissions.add(instance)


@receiver(post_delete, sender=Permission)
def auto_revoke_permission_of_library_admin_group(sender, instance, **kwargs):
    excluded_content_types, library_admin_group = _get_types_and_group()

    if instance.content_type not in excluded_content_types:
        library_admin_group.permissions.remove(instance)
