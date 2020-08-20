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
from .utils import get_read_time, unique_slug_generator


class PostManager(models.Manager):

    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(category__icontains=query)|
                         Q(content__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

    #def get_queryset(self):
    #    return Post.objects.filter(owner=self.kwargs['pk'])

    def get_absolute_url(self):
        return reverse('flock.views.view_single_flock', args=[str(self.pk)])

    def flock_owner(self):
        return reverse('accounts.views.view_profile_with_pk', args=[str(self.user)])

    def type_filter(self):
        return reverse('flock.views.filter_flock_type', args=[str(self.flock_type)])


    # def get_api_url(self):
    #     return reverse("posts-api:detail", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("flock:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        return reverse("flock:like-api-toggle", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def edit_job(self):
        job = Post.objects.update(args=[str(self.id)])
        return reverse('jobs:view_all_jobs', job)


    def upload_location(instance, filename):
        PostModel = instance.__class__
        new_id = PostModel.objects.order_by("id").last().id + 1
        return "%s/%s" %(new_id, filename)
