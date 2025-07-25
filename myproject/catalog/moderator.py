from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Product


@receiver(post_migrate)
def create_moderator_group(sender, **kwargs):
    group, created = Group.objects.get_or_create(name='Модератор продуктов')
    content_type = ContentType.objects.get_for_model(Product)

    permissions = Permission.objects.filter(
        content_type=content_type,
        codename__in=['can_unpublish_product','can_publish_product', 'delete_product']
    )
    group.permissions.set(permissions)
