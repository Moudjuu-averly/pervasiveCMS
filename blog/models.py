# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from django.urls import reverse
from django.utils.safestring import mark_safe
from autoslug import AutoSlugField
from ckeditor_uploader.fields import  RichTextUploadingField
from .manager import BlogPostManager

class BlogPost(models.Model):
    #blog type choices
    EVENT                    = 'E'
    NEWS                     = 'N'
    BLOG_TYPE_CHOICES = (
        (EVENT, 'Event'),
        (NEWS, 'News'),

    )

    #short details
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_tittle           = models.CharField(max_length=255, null=False)
    slug                  = AutoSlugField(unique=True, editable=True, populate_from='blog_tittle',
                        unique_with=['user', 'created'])
    content               = RichTextUploadingField()
    blog_category         = models.CharField(
                                max_length=1,
                                choices=BLOG_TYPE_CHOICES,
                                default=NEWS,
            )
    blog_image            = models.FileField(upload_to='images/blogpost/images', null=True, blank=True)
    rating                = models.FloatField(blank=False, null=True)#suppose is a ForeignKey field
    views                 = models.IntegerField(blank=True, null=True, default=0)#
    view_by               = models.GenericIPAddressField(default='127.0.0.1')
    deleted               = models.BooleanField(default=False)
    edited                = models.BooleanField(default=False)
    #time and date
    created               = models.DateTimeField(auto_now_add=True)
    last_edited           = models.DateTimeField(auto_now=True)
    last_accessed         = models.DateTimeField(auto_now=True)
    active                = models.BooleanField(default=True)

    #call the manager
    objects              = BlogPostManager()

    class Meta:
        ordering         = ('-created', '-last_edited' )

    def __str__(self):
        return "{0}-{1}".format(self.user, self.blog_tittle)



def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique__slug_generator(instance)

post_save.connect(post_save_receiver, sender=BlogPost)
