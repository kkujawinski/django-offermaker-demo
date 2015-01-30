# -*- coding: utf-8 -*-

import json
import random

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group

import offermaker
from .models import (DemoOfferMakerForm, Offer)


given_names = ['Nicolas', 'Diego', 'Jackson', 'Mason', 'Daniel', 'Ethan', 'Santiago', 'Christian', 'Matias',
               'Samuel', 'William', 'Elijah', 'Jack', 'Jacob', 'Luis', 'Isaiah', 'Alexander', 'Josiah', 'Lucas',
               'Gabriel', 'Michael', 'Sebastian', 'Jeremiah', 'Joshua', 'Noah', 'Aiden', 'Mateo', 'Tyler',
               'Jayden', 'Liam']


def _extra_request_params(request):
    user = request.user
    if user.is_superuser:
        all_offers = Offer.objects.all()
    else:
        general_offers = Offer.objects.filter(id__lte=3)
        if user.id:
            my_offers = Offer.objects.filter(user=request.user)
            all_offers = general_offers | my_offers
        else:
            all_offers = general_offers
    return {'all_offers': all_offers}


def _offer_form(template):
    def fn(request):
        params = _extra_request_params(request)
        id_param = request.GET.get('id')
        selected = params['all_offers'].filter(id=id_param).first() if id_param else params['all_offers'].first()
        if selected is None:
            raise Exception("No such offer")
        core_object = offermaker.OfferMakerCore(DemoOfferMakerForm, selected.offer)

        def handler_get(form):
            params.update({'form': form, 'offer': core_object, 'selected': selected})
            return render(request, template, params)

        def handler_post(form):
            if form.is_valid():
                return HttpResponseRedirect('/')
            return handler_get(form)

        dispatcher = offermaker.OfferMakerDispatcher.from_core_object(
            handler_get,
            handler_post,
            core_object=core_object
        )
        return dispatcher.handle_request(request)
    return fn

offer_form = _offer_form('offermaker_form.html')

offer_form_vanilla = _offer_form('offermaker_nobootstrap.html')


def editor(request):
    params = _extra_request_params(request)
    return render(request, 'offermaker_editor.html', params)


def how_to(request):
    params = _extra_request_params(request)
    return render(request, 'offermaker_howto.html', params)


def generate_user(request):
    if request.method == 'POST':
        try:
            last_user_id = User.objects.latest('id').id
        except User.DoesNotExist:
            last_user_id = 0

        username = '%s%d%02d' % (random.choice(given_names), random.randint(10, 99), last_user_id)
        password = str(random.randint(1000, 9999))
        json_output = json.dumps({'username': username, 'password': password})

        user = User.objects.create_user(username, '', password)
        user.groups.add(Group.objects.filter(name='demo').first())
        user.is_staff = True
        user.save()

        return HttpResponse(json_output, content_type="application/json")
    return HttpResponseRedirect('/')
