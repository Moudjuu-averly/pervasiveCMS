# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import *
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from .manager import ServiceManager
from ckeditor_uploader.fields import  RichTextUploadingField
from autoslug import AutoSlugField


class Service(models.Model):
    #service type choices
    CONSULTANT              = '1'
    COUNCELLING             = '2'
    BEAUTY_N_FASHION        = '3'
    EDUCATION               = '4' # L for Freelancer
    FINANCIAL               = '5'
    TRANSPORTATION          = '6'
    ELECTRONICS             = '7'
    INTERNET                = '8'
    OTHER                   = '9'
    SERVICE_CATEGORY_CHOICES = (
        (CONSULTANT, 'Consultant'),
        (COUNCELLING, 'Councelling'),
        (BEAUTY_N_FASHION, 'Beauty and fashion'),
        (EDUCATION, 'Education'),
        (FINANCIAL, 'Financial'),
        (TRANSPORTATION, 'Transportation'),
        (ELECTRONICS, 'Electronics'),
        (INTERNET, 'Internet'),
        (OTHER, 'Other'),
    )

    NORMAL      = '1'
    SPECIAL     = '2'
    PROMO       = '3'
    OFFERTYPE = (
        (NORMAL, 'Normal'),
        (SPECIAL, 'Special'),
        (PROMO, 'Promo'),

    )
    #short details
    user                        = models.ForeignKey(User, on_delete=models.CASCADE)
    service_tittle              = models.CharField(max_length=255, null=False)
    slug                        = AutoSlugField(unique=True, editable=True, populate_from='service_tittle',
                        unique_with=['user', 'created'])
    content               = RichTextUploadingField()
    service_type                = models.CharField(
                                max_length=1,
                                choices=SERVICE_CATEGORY_CHOICES,
                                default=CONSULTANT,
            )
    offer_type                    = models.CharField(
                                max_length=1,
                                choices=OFFERTYPE,
                                default=NORMAL,
            )
    service_video               = models.FileField(upload_to='videos/services/service_video', null=True, blank=True)
    rating                      = models.FloatField(blank=False, null=True)#suppose is a ForeignKey field
    views                       = models.IntegerField(blank=True, null=True, default=0)#
    view_by                     = models.GenericIPAddressField(default='127.0.0.1')
    deleted                     = models.BooleanField(default=False)
    edited                      = models.BooleanField(default=False)

    #prices
    start_price                 = models.FloatField(blank=False, null=False, default=150.00)
    end_price                   = models.FloatField(blank=False, null=True)

    #time and date
    created                     = models.DateTimeField(auto_now_add=True)
    last_edited                 = models.DateTimeField(auto_now=True)
    last_accessed               = models.DateTimeField(auto_now=True)
    active                      = models.BooleanField(default=True)

    #call the manager
    objects                     = ServiceManager()

    class Meta:
        ordering         = ('-created', '-last_edited' )

    def __str__(self):
        return '%s %s' % (self.service_tittle, self.user)

    def __unicode__(self):
        return str(self.service_video)

    @classmethod
    def message(cls, today): pass
        #date = datetime.date()
        #today = timezone.now()
        #days_left = self.due_date - today
        #if today < instance.due_date:
        #    message = 'Due in ' + days_left + '\s'
        #else:
        #    message = 'Due Today'

#observer design parten
# def pre_save_post_due_date_monitor_receiver(sender, instance, *args, **kwargs):
#     date = datetime.date()
#     if instance.due_date.date() < date.today():
#         instance.active = False
# pre_save.connect(pre_save_post_due_date_monitor_receiver, sender=Postservice)
