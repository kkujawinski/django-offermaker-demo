# -*- coding: utf-8 -*-

from django.contrib import admin
from . import models


class OfferAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name', 'user')
    fields = ('name', 'offer')

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(OfferAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True

    def queryset(self, request):
        if request.user.is_superuser:
            return models.Offer.objects.all()
        return models.Offer.objects.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


admin.site.register(models.Offer, OfferAdmin)
