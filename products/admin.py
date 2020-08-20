# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from . models import Product
from django.contrib.auth.models import User
from django.db.models.signals import post_save



# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        Model = Product
        fields = ('__all__')


# def create_job_profile(sender, **kwargs):
#     if kwargs['created']:
#         job_profile = PostJob.objects.create(user=kwargs['instance'])

#post_save.connect(create_job_profile, sender=User)


admin.site.register(Product)
