# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import timedelta, time
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from django.utils.text import slugify


class ProfileQuerySet(models.QuerySet):
#    def smaller_than(self, size):
#        return self.filter(size__lt=size)

#    def active(self):
#        return self.filter(active=True)
    def full_time(self):
        return self.filter(service_type='F')

    def part_time(self):
        return self.filter(service_type='P')

    def contract(self):
        return self.filter(service_type='C')

    def freelancer(self):
        return self.filter(service_type='L')

    def internship(self):
        return self.filter(service_type='I')

    def volunteer(self):
        return self.filter(service_type='V')

    def active(self): pass


    def trending(self, num = 3):
        return sefl.filter(rating__gt=num)


class ServiceManager(models.Manager):
    """docstring for serviceManager."""

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(service_tittle__icontains=query) |
                         Q(service_type__icontains=query)|
                         Q(content__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)  # Important!

    def active(self):
        return self.get_queryset().active()

    @classmethod
    def clean(self):pass
        #today = datetime.date.today()
        #if self.due_date is None and  self.due_date <= today:
        #    raise ValidationError(_('Due date must be a future date.'))

    def get_absolute_url(self):
        return reverse('services.views.view_single_service', kwargs={"slug": self.slug})

    def service_owner(self):
        return reverse('profiles:view_profile_with_pk', args=[str(self.user.pk)])

    @property
    def type_filter(self):
        return reverse('services:filter_service_type', args=[str(self.service_type)])

    @property
    def type(self):
        return self.get_service_type_display()

    @property
    def total_services(self):
        #Places.objects.count()
        return self.objects.filter(active=True).count()

    def all_services(self):
        all_services            = self.objects.filter(active=True).all().order_by('-created')
        total_services          = self.objects.filter(active=True).count()
        owner_total         = self.objects.filter(active=True, args=[str(self.user.pk)]).count()
        type_total          = self.objects.filter(active=True, args=[str(self.service_type)]).count()

        '''
        Admin queries only
        '''
        quarter_total       = super().active().filter(created__quarter=2).count()
        mon_friday_services     = self.objects.filter(created__week_day__gte=2, created__week_day__lte=6).count()
        weekend_services        = self.objects.filter(created__week_day__gte=6, created__week_day__lte=2).count()

        def average(request):
            all_average     = self.objects.filter(active=True).aggregate(Avg('service_type'))
            all_type = self.objects.filter(active=True, args=[str(self.service_type)]).aggregate(Avg('service_type'))

        def top_services(request):
            above_3         = Count('postservice', filter=Q(postservice__rating__gt=3))
            below_4         = Count('postservice', filter=Q(postservice__rating__lte=4))
            _all            = super().active().annotate(below_4=below_4).annotate(above_3=above_3)
            _top_service        = super().active().all().aggregate(Max('rating'))
            low_rate        = _all[0].above_3
            top_rate        = _all[0].below_4
        return

    def edit_service(self):
        service = Postservice.objects.update(args=[str(self.id)])
        return reverse('services:view_all_services', service)
