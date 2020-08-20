from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from django_countries.fields import CountryField


#Pervasive user profiles
class CompanyProfile(models.Model):
    #user info
    user            = models.OneToOneField(User)
    phone           = models.IntegerField(default=0, blank=True)
    type            = models.CharField(max_length=50, default='', blank=True)
    about           = models.TextField(max_length=120, blank=True)
    website         = models.URLField(null=True, blank=True)

    #address
    company_name         = models.CharField(max_length=100, default='', blank=True)
    city            = models.CharField(max_length=50, default='', blank=True)
    address         = models.CharField(max_length=50, default='', blank=True)
#    country         = CountryField(blank_label='(select country)')

    #media
    profile_image   = models.ImageField(upload_to='media/images/profile_image', null=True, blank=True)
    cover_pic     = models.ImageField(upload_to='media/images/corporate/cover_pic', null=True, blank=True)
    #about_video     = models.FileField(upload_to='media/videos/about_video', null=True, blank=True)
    #about_video     = models.FileField(upload_to='media/videos/flock_cover', null=True, blank=True)

    #tracking the user
    #ip_addres       = forms.GenericIPAddressField()

    def __str__(self):
            return self.user.email

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = CompanyProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class PostJob(models.Model):
    user            = models.ForeignKey(User)
    job_tittle      = models.CharField(max_length=255)
    description     = models.TextField(max_length=140)
    requirements    = models.TextField(max_length=200)
    salary_scale    = models.FloatField(blank=False, null=False)

        #time and date
    created         = models.DateTimeField(auto_now_add=True)
    due_date        = models.DateField(auto_now=False, auto_now_add=False)
    updated         = models.DateTimeField(auto_now=True)

def create_post(sender, **kwargs):
    if kwargs['created']:
        post = Post.objects.create(user=kwargs['instance'])

post_save.connect(create_post, sender=User)
