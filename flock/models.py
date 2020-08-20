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
from ckeditor_uploader.fields import  RichTextUploadingField
from .utils import get_read_time, unique_slug_generator
from .manager import PostManager


class BasePost(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    #time and date, views
    created         = models.DateTimeField(auto_now_add=True)
    #publish         = models.DateField(auto_now=False, auto_now_add=False)
    #read_time       = models.IntegerField(default=0)
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp       = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_accessed   = models.DateTimeField(auto_now_add=True, auto_now=False)
    num_of_views    = models.IntegerField(default=0, null=True)

    class Meta:
        abstract = True
        #ordering = ['name']

class Post(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    title           = models.CharField("Title", max_length=160, null=True, blank=True)
    slug            = models.SlugField(unique=True)
    likes           = models.ManyToManyField(User, blank=True, related_name='post_likes')
    #comments         = models.ForeignKey(Comments, blank=True, related_name='post_comments')
    content               = RichTextUploadingField()

    #category
    category        = models.CharField(max_length=160, null=True, blank=True)
    draft           = models.BooleanField(default=False)
    edited          = models.BooleanField(default=False)

    #media, it should not be blank to avoid too much text on the app
    post_image      = models.FileField("Image", upload_to='media/images/post_images', null=True, blank=True)
    post_video      = models.FileField(upload_to='media/video/post_videos', null=True, blank=True)

    #time and date, views
    created         = models.DateTimeField(auto_now_add=True)
    #publish         = models.DateField(auto_now=False, auto_now_add=False)
    #read_time       = models.IntegerField(default=0)
    updated         = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp       = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_accessed   = models.DateTimeField(auto_now_add=True, auto_now=False)
    num_of_views    = models.IntegerField(default=0, null=True)

    objects         = PostManager()


    def __unicode__(self):
        return "{0}".format(self.title)

    def __str__(self):
        return '%s %s' % (self.title, self.user)

    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug(instance, new_slug=None):
    slug = slugify(self.job_tittle)
    if slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)
#
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
#     if instance.content:
#         read_time_var = get_read_time(instance.content)
#         instance.read_time = read_time_var





class Comments(models.Model):
    text                 = models.TextField(max_length=120, null=True, blank=True)
    post                 = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_by           = models.ManyToManyField(User, related_name='comments_by', blank=True)
    likes                = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')

    #media, it should not be blank to avoid too much text on the app
    comment_image        = models.FileField(upload_to='media/images/comment_image', null=True, blank=True)
    comment_video        = models.FileField(upload_to='media/video/comment_video', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s %s' % (self.comment_by, self.text)

def create_comment(sender,instance, **kwargs):
    if kwargs['created']:
        try:
            comment = Comments.objects.get_or_create(user=kwargs['instance'])
        except:
            pass

post_save.connect(create_comment, sender=User)



class Friend(models.Model):
    users           = models.ManyToManyField(User, symmetrical=False)
    current_user    = models.ForeignKey(User, related_name='flocker', null=True, blank=True, on_delete=models.CASCADE)
    #created         = models.DateTimeField(auto_now_add=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

def create_friend(sender,instance, **kwargs):
    if kwargs['created']:

        try:
            friend = Friend.objects.create(user=kwargs['instance'])
        except:
            pass


post_save.connect(create_friend, sender=User)
