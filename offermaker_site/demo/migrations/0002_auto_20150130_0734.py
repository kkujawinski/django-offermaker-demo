# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations


def create_demo_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    offer_permissions = Permission.objects.filter(content_type__name='offer')
    group, created = Group.objects.get_or_create(name='demo')
    if created:
        group.permissions.add(*offer_permissions)


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_demo_group
        ),
    ]
