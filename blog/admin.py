# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from blog.models import BlogPost
from .manager import BlogPostManager
from .utils import *
from django.db.models.signals import post_save, pre_save

# Register your models here.
def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_announce_slug_generator(instance)

post_save.connect(post_save_receiver, sender=BlogPost)


admin.site.register(BlogPost)
