# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from .manager import SupportManager


class Support(models.Model):
    #SUPPORT type choices
    TECHNICAL       = 'T'
    PLANS           = 'PL'
    SECURITY        = 'S'
    DESIGN          = 'D'
    ADVERTS         = 'A'
    PROFILE         = 'P'
    OTHERS          = 'O'
    SUPPORT_TYPE_CHOICES = (
        (TECHNICAL, 'Technical'),
        (PLANS, 'Plans'),
        (SECURITY, 'Security'),
        (DESIGN, 'Design'),
        (ADVERTS, 'Adverts'),
        (PROFILE, 'Profile/ Account'),
        (OTHERS, 'Others'),
    )

    #short details
    user                  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders')
    support_tittle        = models.CharField(max_length=255, null=False)
    content               = models.CharField(max_length=500, null=False)
    image                 = models.FileField(upload_to='support/images', null=True, blank=True)
    support_type          = models.CharField(
                                max_length=1,
                                choices=SUPPORT_TYPE_CHOICES,
                                default=TECHNICAL,
            )
    viewed_by_ip            = models.GenericIPAddressField(default='127.0.0.1')
    #time and date
    created               = models.DateTimeField(auto_now_add=True)
    seen                  = models.BooleanField(default=True)
    seen_by_us            = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at               = models.DateTimeField(auto_now=True)

    #call the manager
    objects              = SupportManager()

    class Meta:
        ordering         = ('-created', )

    def __str__(self):
        return '%s %s' % (self.support_tittle, self.user)
