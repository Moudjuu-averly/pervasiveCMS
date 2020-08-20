# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin import AdminSite
from accounts.models import DefaultImg, SocialProfiles
from django.db.models.signals import post_save

class MyAdminSite(AdminSite):
    site_header = 'Flock Inc accounts Analytics'


class UserDefaultImg(admin.ModelAdmin):
    class Meta:
        Model = DefaultImg
        fields = ('__all__')

class UserSocialProfiles(admin.ModelAdmin):
    class Meta:
        Model = SocialProfiles
        fields = ('__all__')


def create_social_profile(sender, **kwargs):
    if kwargs['created']:
        try:
            user_social_profile = SocialProfiles.objects.create(user=kwargs['instance'])
        except:
            pass

post_save.connect(create_social_profile, sender=User)
admin.site.register(SocialProfiles, UserSocialProfiles)


admin_site = MyAdminSite(name='flock-inc-admin')
admin.site.register(DefaultImg, UserDefaultImg)
