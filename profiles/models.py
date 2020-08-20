from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
#from finance.models import UserMembership
from django_countries.fields import CountryField
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from django.shortcuts import render, get_object_or_404, redirect
from .manager import ProfileManager
from autoslug import AutoSlugField
from autoslug.settings import slugify as default_slugify
from ckeditor_uploader.fields import  RichTextUploadingField


    # def active(self):
    #     from django.utils import timezone
    #     for e in self.objects.filter(args=[str(self.user.pk)]):
    #         today                   = date.today()
    #         if e.due_date           == today:
    #             e.active                = True
    #             display_text        = 'Due today.'
    #         elif not e.due_date     <= today:
    #             e.active                = True
    #             display_text        = 'Due in ' + date(count(due_date - today)) + ' days\'s.'
    #         else:
    #             self.active         = False
    #         return

class Profile(models.Model):
    '''
    Company Profile
    '''
    CONSULTING          = 'CONSULTING'
    CELEBRITY           = 'CELEBRITY'
    CONTRACT            = 'CONTRACT'
    MEDIA               = 'MEDIA'
    ELECTRONICS         = 'ELECTRONICS'
    ENTERTAINMENT       = 'ENTERTAINMENT'
    INFORMATION_TECH    = 'INFORMATION'
    OTHERS              = 'OTHERS'

    BUS_TYPE_CHOICES = (
        (CONSULTING, 'Consulting'),
        (CELEBRITY, 'Celebrity'),
        (CONTRACT, 'Contract'),
        (MEDIA, 'Media'),
        (ELECTRONICS, 'Electronics'),
        (ENTERTAINMENT, 'Entertainment'),
        (INFORMATION_TECH, 'Information Technology'),
        (OTHERS, 'Others'),
    )
    business_type              = models.CharField(
                                max_length=50,
                                choices=BUS_TYPE_CHOICES,
                                default=OTHERS, null=True
            )
    official_business_name      = models.CharField(max_length=50, null=True,  blank=True)
    slug                        = AutoSlugField(unique=True, editable=True, populate_from='official_business_name',
                        unique_with=['user'], default='', null=True, blank=True)
    #member                     = models.OneToOneField(UserMembership, on_delete=models.CASCADE,null=True, unique=True, default='Starter')
    prefered_language           = models.CharField(max_length=10,
                                choices=settings.LANGUAGES,
                                default=settings.LANGUAGE_CODE)

    # There is an inherent relationship between the Profile and
    # User models. By creating a one-to-one relationship between the two, we
    # are formalizing this relationship. Every user will have one -- and only
    # one -- related Profile model.
    user                        = models.OneToOneField(User, on_delete=models.CASCADE)
    likes                       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='profile_likes')
    rated                       = models.IntegerField( null=True)
    views                       = models.IntegerField( null=True)

    #company info details
    country_origin              = CountryField(blank_label='(select country)', default='--select country--')
    country_city                = models.CharField(max_length=255, default='', null=True, blank=True)
    #zip_code                    = models.IntegerField(default=0, blank=True)
    office_phone                = models.IntegerField(default=0, blank=True)
    contact_cell                = models.IntegerField(default=0, blank=True)
    email_address               = models.CharField(max_length=255, default='', null=True, blank=True)
    support_email               = models.CharField(max_length=255, default='', null=True, blank=True)
    sales_email                 = models.CharField(max_length=255, default='', null=True, blank=True)
    info_email                  = models.CharField(max_length=255, default='', null=True, blank=True)
    about                       = RichTextUploadingField()
    address                     = models.CharField(max_length=255, default='', null=True,blank=True)
    location                    = models.CharField(max_length=255, default='', null=True, blank=True)

    #tracking the update location country-city
    update_ip_addres            = models.GenericIPAddressField(default='127.0.0.1')
    #viewed by
    viewed_by                   = models.GenericIPAddressField(default='127.0.0.1')


    #commented fields are not for a regular package
    website                     = models.URLField(null=True, blank=True)
    other_website               = models.URLField(null=True, blank=True)
    blog                        = models.URLField(null=True, blank=True)

    #Company address capturing
    other_names                 = models.CharField(max_length=50, default='', blank=True)
    company_name                = models.CharField(max_length=100, default='', blank=True)

    #media
    profile_image               = models.ImageField(upload_to='images/profile_image', null=True, blank=True)
    cover_image                 = models.ImageField(upload_to='images/cover_cover', null=True, blank=True)
    about_video                 = models.FileField(upload_to='videos/about_video', null=True, blank=True)
    who_we_are_video            = models.FileField(upload_to='videos/who_we_are_video', null=True, blank=True)
    services_video              = models.FileField(upload_to='videos/services_video', null=True, blank=True)
    projects_video              = models.FileField(upload_to='videos/projects_video', null=True, blank=True)

    #time and date
    created                     = models.DateTimeField(auto_now_add=True)
    updated                     = models.DateTimeField(auto_now=True)

    # NB: important
    '''profile activation and deactivation'''
    active                      = models.BooleanField(default=False)

    objects = ProfileManager()

    class Meta: pass
        #ordering                = ["ip_addres", "-country_city"]

    def __str__(self):
        return '%s %s' % (self.user, self.business_type)

    def __unicode__(self): pass
        # return "{0}".format(self.company)

    def default_slugify(self):pass

        #return default_slugify(value).replace('-', '_')

    #slug = AutoSlugField(slugify=custom_slugify)

#def create_profile(sender, **kwargs):
#    if kwargs['created']:
#        business_profile        = Profile.objects.create(user=kwargs['instance'])

#post_save.connect(create_profile, sender=User)
