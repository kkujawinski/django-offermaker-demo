# -*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.contrib.auth.models import User

import offermaker


class DemoOfferMakerForm(forms.Form):
    product = forms.ChoiceField(
        label=u'Product',
        choices=(
            ('', '---'), ('PROD1', 'Product X'),
            ('PROD2', 'Product Y'), ('PROD3', 'Product Z'),
        ),
        required=False
    )
    crediting_period = forms.ChoiceField(
        label=u'Crediting period',
        choices=(('', '---'), ('12', '12'), ('24', '24'),
                 ('36', '36'), ('48', '48'))
    )
    interest_rate = forms.FloatField(label=u'Interest rate',
                                     min_value=1, max_value=5)
    contribution = forms.FloatField(label=u'Contribution', min_value=0)
    some_field = forms.CharField(label=u'Some field')


class DemoOfferMakerField(offermaker.OfferJSONField):
    form_object = DemoOfferMakerForm()


class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    offer = DemoOfferMakerField()
    user = models.ForeignKey(User, related_name='offers', null=True, blank=True)

    def __str__(self):
        return self.name
