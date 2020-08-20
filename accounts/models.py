from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import slugify
#from finance.models import UserMembership, Membership
#from flock.models import Post


class SocialProfiles(models.Model):
    #user SocialProfiles
    user                     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_profiles')
    facebook                 = models.URLField(null=True, blank=True)
    twitter                  = models.URLField(null=True, blank=True)

    #not for a starter package
    linkedin                 = models.URLField(null=True, blank=True)

    #not for a regular package
    youtube                  = models.URLField(null=True, blank=True)
    instagram                = models.URLField(null=True, blank=True)
    snapchat                 = models.URLField(null=True, blank=True)
    google                   = models.URLField(null=True, blank=True)
    github                   = models.URLField(null=True, blank=True)
    dribble                  = models.URLField(null=True, blank=True)
    reddit                   = models.URLField(null=True, blank=True)
    thumbler                 = models.URLField(null=True, blank=True)

    def __str__(self):
            return "{0}".format(self.user)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = SocialProfiles.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class DefaultImg(models.Model):
    #user info
    #user            = models.ForeignKey(User, on_delete=models.CASCADE)
    basecode_logo     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    profile_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    cover_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    jobs_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    service_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    tender_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    product_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)
    blog_img     = models.ImageField(upload_to='images/defaults', null=True, blank=True)

    def __str__(self):
            return "{0}".format(self.profile_img)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = DefaultImg.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
