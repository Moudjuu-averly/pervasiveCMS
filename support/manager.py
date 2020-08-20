# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from django.db import models


class SupportQuerySet(models.QuerySet):
#    def smaller_than(self, size):
#        return self.filter(size__lt=size)

#    def active(self):
#        return self.filter(active=True)
    def full_time(self):
        return self.filter(job_type='F')

    def part_time(self):
        return self.filter(job_type='P')

    def contract(self):
        return self.filter(job_type='C')

    def freelancer(self):
        return self.filter(job_type='L')

    def internship(self):
        return self.filter(job_type='I')

    def volunteer(self):
        return self.filter(job_type='V')

    def active(self): pass


    def trending(self, num = 3):
        return sefl.filter(rating__gt=num)


class SupportManager(models.Manager):
    """docstring for JobManager."""
    def get_queryset(self):
        return SupportQuerySet(self.model, using=self._db)  # Important!

    def active(self):
        return self.get_queryset().active()

    @classmethod
    def clean(self):pass
        #today = datetime.date.today()
        #if self.due_date is None and  self.due_date <= today:
        #    raise ValidationError(_('Due date must be a future date.'))

    def get_absolute_url(self):
        return reverse('jobs.views.view_single_job', kwargs={"slug": self.slug})


    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def upload_location(instance, filename):
        PostModel = instance.__class__
        new_id = PostModel.objects.order_by("id").last().id + 1
        return "%s/%s" %(new_id, filename)
