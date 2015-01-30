# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import offermaker_site.demo.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('offer', offermaker_site.demo.models.DemoOfferMakerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='offers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
