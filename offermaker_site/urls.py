# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin

from .demo import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^editor/?', views.editor),
    url(r'^generate_user/?', views.generate_user),
    url(r'^how_to/', views.how_to),
    url(r'^form_vanilla$', views.offer_form_vanilla),
    url(r'^form$', views.offer_form),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.*$', views.how_to),
)
