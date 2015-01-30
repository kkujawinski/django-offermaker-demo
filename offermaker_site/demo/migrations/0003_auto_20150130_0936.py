# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_demo_offers(apps, schema_editor):
    Offer = apps.get_model("demo", "Offer")
    Offer.objects.create(
        name='Offer 1',
        offer={
            "variants": [[
                {"params": {"product": "PROD1", "crediting_period": ["24"]}},
                {"params": {"product": "PROD2", "crediting_period": ["12", "36", "48"]}},
                {"params": {"product": "PROD3"}}
            ], [
                {"params": {"product": "PROD1", "contribution": [[10, 20]], "interest_rate": [[2, 2]]}},
                {"params": {"product": "PROD1", "contribution": [[30, 40]], "interest_rate": [[4, 4]]}},
                {"params": {"product": ["PROD2", "PROD3"], "contribution": [[30, 70]], "interest_rate": [[5, 5]]}}
            ]],
            "params": {}
        }
    )
    Offer.objects.create(
        name='Offer 2',
        offer={
            "variants": [[
                {"params": {"product": "PROD3"}},
                {"params": {"product": "PROD1", "crediting_period": ["24"]}},
                {"params": {"product": "PROD2", "crediting_period": ["48"]}}
            ], [
                {"params": {"product": "PROD1", "contribution": [[10, 20]]}},
                {"params": {"product": "PROD1", "interest_rate": [[4, 4]]}},
                {"params": {"product": ["PROD2", "PROD3"], "contribution": [[30, 70]], "interest_rate": [[5, 5]]}}
            ]],
            "params": {}
        }
    )
    Offer.objects.create(
        name='Offer 3',
        offer={
            "variants": [[
                {"params": {"product": "PROD1", "crediting_period": ["12", "24"]}},
                {"params": {"product": "PROD2", "crediting_period": ["36", "48"]}}
            ]],
            "params": {"contribution": [[30, 70]]}
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20150130_0734'),
    ]

    operations = [
        migrations.RunPython(
            create_demo_offers
        ),
    ]
