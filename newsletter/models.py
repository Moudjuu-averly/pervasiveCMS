# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save, pre_save
from . manager import ContactManager
from django.utils.translation import ugettext_lazy as _
from profiles.models import Profile
from django.utils import timezone
#from django.contrib.sites.models import Site
from autoslug import AutoSlugField
from ckeditor_uploader.fields import  RichTextUploadingField



class Join(models.Model):
    email           = models.EmailField(unique=True)
    ip_address      =models.CharField(max_length=120, default='None')
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" %(self.email)

    def clean_mail(self, *args, **kwargs):
        email = super(Join, self).cleaned_data.get("email")
        qs    = Join.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('You\'re already a member, n\'plz check your spam folder. ')
        return email

    def get_absolute_url(self):
        from django.urls import reverse
        #return reverse('accounts.views.view_profile', kwargs={'user':self.slugify(user.username)})
        #return reverse('support.views.subscribers', args=[str(self.id)])

    def get_queryset(self):
        return Join.objects.filter(owner=self.kwargs['pk']).all().order_by('timestamp')

class Contact(models.Model):
    #SUPPORT type choices
    TECHNICAL       = 'T'
    PLANS           = 'PL'
    SECURITY        = 'S'
    DESIGN          = 'D'
    ADVERTS         = 'A'
    PROFILE         = 'P'
    OTHERS          = 'O'
    CONTACT_TYPE_CHOICES = (
        (TECHNICAL, 'Technical'),
        (PLANS, 'Plans'),
        (SECURITY, 'Security'),
        (DESIGN, 'Design'),
        (ADVERTS, 'Adverts'),
        (PROFILE, 'Profile/ Account'),
        (OTHERS, 'Others'),
    )

    to              = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name       = models.CharField(max_length=50)
    email           = models.EmailField(max_length=50)
    subject         = models.CharField(
                        max_length=50,
                        choices=CONTACT_TYPE_CHOICES,
                        default=TECHNICAL,
    )
    message         = models.TextField(max_length=1250)
    subject         = models.CharField(max_length=150)
    ip_address      = models.GenericIPAddressField()
    created         = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)

    objects = ContactManager()

    def __unicode__(self):
        return "%s - %s" %(self.email, seff.full_name)

    class Meta:
        ordering         = ('-created', )

    #def clean_contact(self, *args, **kwargs):

    #    form_email       = self.cleaned_data.get("email")
        #check nlacklisted emails
        #qs    = Blacklisted.objects.filter(email__iexact=email)
        #if qs.exists():
        #    black_message = 'This email has been blacklisted from contacting this company please' +
        #    'contact ' + to.user.BusinessBaseProfile.help_email to resolve the issue +''
        #    raise forms.ValidationError(black_message)
        #return email

    #    form_full_name   = self.cleaned_data.get("full_name")
    #    form_message     = self.cleaned_data.get("message")

    def get_absolute_url(self):
        from django.urls import reverse
        #return reverse('accounts.views.view_profile', kwargs={'user':self.slugify(user.username)})
        #return reverse('support.views.subscribers', args=[str(self.id)])

    def get_queryset(self):
        return Contact.objects.filter(owner=self.kwargs['pk']).all().order_by('timestamp')


class Subscribe(models.Model):
    to              = models.OneToOneField(User, on_delete=models.CASCADE)
    email           = models.EmailField(max_length=150)
    ip_address      = models.CharField(max_length=120, default='None')
    timestamp       = models.DateTimeField(auto_now_add=True)
    active          = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" %(self.email)

    def clean_subscribe(self, *args, **kwargs):

        email               = self.cleaned_data.get("email")
        #check blacklisted emails
        qs                  = Subscribe.objects.filter(email__iexact=email).filter(active=False)
        if qs.exists():
            #black_message   = 'This email has been blacklisted from contacting this company please' +
            #'contact ' + to.user.BusinessBaseProfile.support_email  +'to resolve the issue'
            raise forms.ValidationError('this email already exists, pls check your spam folder.')
        return email

    def blocking(self, *args, **kwargs):
        if self.email:
            if self.active  == True:
                self.active = False
            else:
                self.active = True
            return self.email
        return

    def get_absolute_url(self):
        from django.urls import reverse
        #return reverse('support.views.subscribers', args=[str(self.id)])

    def get_queryset(self):
        return Subscribe.objects.filter(owner=self.kwargs['pk']).all().order_by('timestamp')

class Subscription(models.Model):
      email=models.EmailField(_('email address'),primary_key=True,max_length=254)
      is_active=models.BooleanField(_('is active'),default=True)
      created=models.DateField(auto_now_add=True)
      #objects=models.Manager()


class PostMail(models.Model):
      STATUS_CHOICES=(
          ('draft','Draft'),
          ('published','Published')
      )
      #tags=TaggableManager()
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      #category=models.ForeignKey(Category,default=1,on_delete=models.CASCADE,related_name='posts')
      tittle=models.CharField(max_length=250)
      slug=AutoSlugField(unique=True, editable=True, populate_from='tittle',
                          unique_with=['user', 'created'])
      #author=models.ForeignKey(User,related_name='user',default=1,on_delete=models.CASCADE)
      content               = RichTextUploadingField()
      short_description = models.CharField(max_length=800,blank=True,null=True)
      created=models.DateTimeField(default=timezone.now)
      post_file = models.FileField(upload_to='media/posts/',blank=True)
      created=models.DateTimeField(auto_now_add=True)
      updated=models.DateTimeField(auto_now=True)
      #status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
      mainimage = models.ImageField(upload_to='media/',blank=True)
      #number_of_click=models.PositiveIntegerField(default=0)

      #objects=models.Manager()

      class Meta:
          ordering=('-created',)

      def __str__(self):
          return self.tittle

      def get_absolute_url(self): pass
          #return reverse('post-detail',
          #args=[self.slug])
      #def get_tag_names(self):
        #  return self.tags.all()

      @property
      def image_file(self):
          return self.mainimage.path

class ContactManager(models.Manager):
    def create_request(self,active, full_name, email, subject, message):
        request = self.create(
                    #request_number=request_number,
                    active=active,
                    full_name=full_name,
                    email=email,
                    subject=subject,
                    message=message
                    )
        return request
