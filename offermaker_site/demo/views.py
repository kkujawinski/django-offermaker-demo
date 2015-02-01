# -*- coding: utf-8 -*-

import json
import random

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.utils.functional import cached_property
from django.views.generic import TemplateView

import offermaker
from .models import DemoOfferMakerForm, Offer


given_names = ['Nicolas', 'Diego', 'Jackson', 'Mason', 'Daniel', 'Ethan', 'Santiago', 'Christian', 'Matias',
               'Samuel', 'William', 'Elijah', 'Jack', 'Jacob', 'Luis', 'Isaiah', 'Alexander', 'Josiah', 'Lucas',
               'Gabriel', 'Michael', 'Sebastian', 'Jeremiah', 'Joshua', 'Noah', 'Aiden', 'Mateo', 'Tyler',
               'Jayden', 'Liam']


def _get_offer_list(request):
    user = request.user
    if user.is_superuser:
        offer_list = Offer.objects.all()
    else:
        general_offers = Offer.objects.filter(user__isnull=True)
        if user.id:
            my_offers = Offer.objects.filter(user=request.user)
            offer_list = general_offers | my_offers
        else:
            offer_list = general_offers
    return offer_list


def _offer_form(template):
    def fn(request):
        params = {'all_offers': _get_offer_list(request)}
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


class SelectedOfferFormView(offermaker.OfferMakerFormView):
    form_class = DemoOfferMakerForm
    template_name = 'offermaker_form.html'

    @property
    def offermaker_offer(self):
        return self.selected_offer.offer

    def dispatch(self, request, *args, **kwargs):
        self.offer_list = _get_offer_list(request)
        id_param = request.GET.get('id')
        if id_param:
            self.selected_offer = self.offer_list.filter(id=id_param).first()
        else:
            self.selected_offer = self.offer_list.first()
        return super(SelectedOfferFormView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SelectedOfferFormView, self).get_context_data(**kwargs)
        context['offer_list'] = self.offer_list
        context['selected'] = self.selected_offer
        return context

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        response = super(SelectedOfferFormView, self).form_valid(form)
        messages.success(self.request, 'Form has been saved')
        return response


offer_form = SelectedOfferFormView.as_view()


def editor(request):
    params = {'all_offers': _get_offer_list(request)}
    return render(request, 'offermaker_editor.html', params)


def how_to(request):
    params = {'all_offers': _get_offer_list(request)}
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
