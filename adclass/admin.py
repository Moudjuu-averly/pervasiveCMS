# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . models import TenderApplicant, Tender, Scholarship, Announce

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        Model = Tender
        fields = ('__all__')

# def create_job_profile(sender, **kwargs):
#     if kwargs['created']:
#         job_profile = PostJob.objects.create(user=kwargs['instance'])

admin.site.register(Announce)
admin.site.register(TenderApplicant)
admin.site.register(Tender)
admin.site.register(Scholarship)
