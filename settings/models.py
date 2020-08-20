# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Settings(models.Model):
    # ...
    user                                = models.OneToOneField(User, on_delete=models.CASCADE)
    language                            = models.CharField(max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)

    #allow_notifications                = models.IntegerField(default=0, blank=True)
    #allow_tags_notifications           = models.IntegerField(default=0, blank=True)

    #tags                               = models.CharField(max_length=50, default='', blank=True)
    #allow_anonymous_message            = models.TextField(max_length=120, blank=True)
    #theme_color                        = models.CharField(null=True, blank=True)
    #blog                               = models.URLField(null=True, blank=True)
    #updated                            = models.DateTImeField(auto_now=True, auto_add_now=True)

    def __init__(self):
        return self.language
