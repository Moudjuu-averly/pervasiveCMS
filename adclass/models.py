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
#from profiles.models import Profile
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from autoslug import AutoSlugField
from .manager import TenderManager, AnnounceManager
from django.utils.text import slugify
from ckeditor_uploader.fields import  RichTextUploadingField

class Tender(models.Model):
    '''
    Tender creation model
    '''
    #short details
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    tender_tittle         = models.CharField(max_length=255, null=False)
    slug                  = AutoSlugField(unique=True, editable=True, populate_from='tender_tittle',
                        unique_with=['user', 'created'])
    content               = RichTextUploadingField()
    advtised_before       = models.BooleanField(default=False)
    tender_video          = models.FileField(upload_to='videos/adclass/tender_video', null=True, blank=True)

    #contact details
    contact_person_name   = models.CharField(max_length=500, null=False, default='')
    office_no             = models.IntegerField(null=False, default='')
    address               = models.CharField(max_length=100, null=False, default='')

    #location
    city                  = models.CharField(max_length=255, null=False, default='')

    #salary
    levy_price            = models.FloatField(default=500, null=True)

    #applicants            = models.ForeignKey(TenderApplicant, on_delete=models.CASCADE, null=True)

    #analytics
    views                 = models.IntegerField(blank=True, null=True, default=0)#
    view_by               = models.GenericIPAddressField(default='127.0.0.1')

    #time and dates
    created               = models.DateTimeField(auto_now_add=True)
    due_date              = models.DateField(auto_now=False, auto_now_add=False, null=True)
    updated               = models.DateTimeField(auto_now=True)
    active                = models.BooleanField(default=True)
    edited                = models.BooleanField(default=False)
    deleted               = models.BooleanField(default=False)

    objects               = TenderManager()

    def __str__(self):
            return "{0} {1}".format(self.user, self.tender_tittle)

def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

post_save.connect(post_save_receiver, sender=Tender)


class TenderApplicant(models.Model):
    '''
    Tender appliocation model
    '''
    #short details
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    application_file      = models.FileField(upload_to='uploads/docs/tender_doc_files', null=True, blank=True)#change null to false
    solution_video        = models.FileField(upload_to='uploads/docs/solution_video', null=True, blank=True)#change null to false
    similar_work_video    = models.FileField(upload_to='videos/docs/similar_tender_video', null=True, blank=True)#change null to false

    #analytics
    times_viewed          = models.IntegerField(blank=True, null=True, default=0)#
    seen                  = models.GenericIPAddressField(default='127.0.0.1')
    #time and date
    created               = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return "{0}-{1}".format(self.user, self.created)

    def get_absolute_url(self):
        from django.urls import reverse
        #return reverse('adclass:view_tender', args=[str(self.id)])


class Scholarship(models.Model):

    #short details
    user                  = models.OneToOneField(User, on_delete=models.CASCADE)
    tittle                = models.CharField(max_length=255, null=False)
    required_docs         = models.TextField(max_length=140, null=False)
    slug                  = AutoSlugField(unique=True, editable=True, populate_from='tittle',
                            unique_with=['user', 'created'])
    applicants            = models.ManyToManyField(User, related_name='applicants')
    content               = RichTextUploadingField()

    #analytics
    views                 = models.IntegerField(blank=True, null=True, default=0)#
    view_by               = models.GenericIPAddressField(default='127.0.0.1')

    #location
    country               = CountryField(blank_label='(select country)', default='--select--', null=False)
    city                  = models.CharField(max_length=255, null=False, default='')

    #time and date
    created               = models.DateTimeField(auto_now_add=True)
    start_date            = models.DateField(auto_now=False, auto_now_add=False, null=True)
    due_date              = models.DateField(auto_now=False, auto_now_add=False, null=True)
    updated               = models.DateTimeField(auto_now=True)
    active                = models.BooleanField(default=True)
    edited                = models.BooleanField(default=False)

    #objects              = ScholarshipManager()

    def __str__(self):
            return "{0}".format(self.user)

    def get_absolute_url(self):
        from django.urls import reverse
        #return reverse('adclass:view_scholarship', args=[str(self.id)])


class Announce(models.Model):
    #announce type choices
    EXPRESSION_OF_INTEREST   = 'E'
    EVENT                    = 'EV'
    BID                      = 'B'
    NEWS                     = 'N'
    ANNOUNCE_TYPE_CHOICES = (
        (EXPRESSION_OF_INTEREST, 'Expression of interest'),
        (EVENT, 'Event'),
        (BID, 'Bid'),
        (NEWS, 'News'),

    )

    #short details
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    announce_tittle       = models.CharField(max_length=255, null=False)
    slug                  = AutoSlugField(unique=True, editable=True, populate_from='announce_tittle',
                        unique_with=['user', 'created'])
    content               = RichTextUploadingField()
    announce_type              = models.CharField(
                                max_length=50,
                                choices=ANNOUNCE_TYPE_CHOICES,
                                default=EVENT,
            )
    announce_image        = models.FileField(upload_to='images/announce/announce_image', null=True, blank=True)
    rating                = models.FloatField(blank=False, null=True)#suppose is a ForeignKey field
    views                 = models.IntegerField(blank=True, null=True, default=0)#
    view_by               = models.GenericIPAddressField(default='127.0.0.1')
    deleted               = models.BooleanField(default=False)
    edited                = models.BooleanField(default=False)
    #time and date
    created               = models.DateTimeField(auto_now_add=True)
    due_date              = models.DateField(auto_now=False, auto_now_add=False, null=True)
    last_edited           = models.DateTimeField(auto_now=True)
    last_accessed         = models.DateTimeField(auto_now=True)
    active                = models.BooleanField(default=True)

    #call the manager
    objects              = AnnounceManager()

    class Meta:
        ordering         = ('-created', '-last_edited' )

    def __str__(self):
        return "{0}-{1}".format(self.user, self.announce_tittle)



def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_announce_slug_generator(instance)

post_save.connect(post_save_receiver, sender=Announce)
