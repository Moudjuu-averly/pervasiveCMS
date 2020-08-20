# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import *
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from .manager import JobManager
from autoslug import AutoSlugField
from ckeditor_uploader.fields import  RichTextUploadingField


class PostJob(models.Model):
    #Job type choices
    FULL_TIME   = 'F'
    PART_TIME   = 'P'
    CONTRACT    = 'C'
    FREELANCER  = 'L' # L for Freelancer
    INTERNSHIP  = 'I'
    VOLUNTEER   = 'V'
    JOB_TYPE_CHOICES = (
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
        (CONTRACT, 'Contract'),
        (FREELANCER, 'Freelancer'),
        (INTERNSHIP, 'Internship'),
        (VOLUNTEER, 'Volunteer'),
    )

    OFFICE   = 'O'
    REMOTE   = 'R'
    LOCATION = (
        (OFFICE, 'Office'),
        (REMOTE, 'Remote'),

    )
    #short details
    user                  = models.ForeignKey(User, on_delete=models.CASCADE)
    job_tittle            = models.CharField(max_length=255, null=False)
    slug                  = AutoSlugField(unique=True, editable=True, populate_from='job_tittle',
                        unique_with=['user', 'created'])
    content               = RichTextUploadingField()
    job_type              = models.CharField(
                                max_length=50,
                                choices=JOB_TYPE_CHOICES,
                                default=FULL_TIME,
            )
    location              = models.CharField(
                                max_length=15,
                                choices=LOCATION,
                                default=OFFICE,
            )
    job_video             = models.FileField(upload_to='videos/jobs/job_video', null=True, blank=True)
    rating                = models.FloatField(blank=False, null=True)#suppose is a ForeignKey field
    views                 = models.IntegerField(blank=True, null=True, default=0)#
    view_by               = models.GenericIPAddressField(default='127.0.0.1')
    deleted               = models.BooleanField(default=False)
    edited                = models.BooleanField(default=False)
    #salary
    min_salary            = models.FloatField(blank=False, null=False, default=150.00)
    max_salary            = models.FloatField(blank=False, null=True)
    #time and date
    created               = models.DateTimeField(auto_now_add=True)
    due_date              = models.DateField(auto_now=False, auto_now_add=False, null=True)
    last_edited           = models.DateTimeField(auto_now=True)
    last_accessed         = models.DateTimeField(auto_now=True)
    active                = models.BooleanField(default=True)

    #call the manager
    objects              = JobManager()

    class Meta:
        ordering         = ('-created', '-last_edited' )

    def __str__(self):
        return '%s %s' % (self.job_tittle, self.user)

    def __unicode__(self):
        return str(self.job_video)

    @classmethod
    def message(cls, today): pass



class RePostJob(models.Model):
    #Job type choices
    FULL_TIME   = 'F'
    PART_TIME   = 'P'
    CONTRACT    = 'C'
    FREELANCER  = 'L' # L for Freelancer
    INTERNSHIP  = 'I'
    VOLUNTEER   = 'V'
    JOB_TYPE_CHOICES = (
        (FULL_TIME, 'Full time'),
        (PART_TIME, 'Part time'),
        (CONTRACT, 'Contract'),
        (FREELANCER, 'Freelancer'),
        (INTERNSHIP, 'Internship'),
        (VOLUNTEER, 'Volunteer'),
    )

    OFFICE   = 'O'
    REMOTE   = 'R'
    LOCATION = (
        (OFFICE, 'Office'),
        (REMOTE, 'Remote'),

    )
    #short details
    company            = models.CharField(max_length=255, null=False)
    job_tittle            = models.CharField(max_length=255, null=False)
    slug                  = AutoSlugField(unique=True, editable=True, populate_from='job_tittle',
                        unique_with=[ 'company', 'created'])
    content               = RichTextUploadingField()
    job_type              = models.CharField(
                                max_length=50,
                                choices=JOB_TYPE_CHOICES,
                                default=FULL_TIME,
            )
    location              = models.CharField(
                                max_length=15,
                                choices=LOCATION,
                                default=OFFICE,
            )
    job_image             = models.FileField(upload_to='images/jobs/job_image', null=True, blank=True)
    rating                = models.FloatField(blank=False, null=True)#suppose is a ForeignKey field
    views                 = models.IntegerField(blank=True, null=True, default=0)#
    view_by               = models.GenericIPAddressField(default='')
    deleted               = models.BooleanField(default=False)
    edited                = models.BooleanField(default=False)
    #salary
    min_salary            = models.FloatField(blank=False, null=False, default=150.00)
    max_salary            = models.FloatField(blank=False, null=True)
    #time and date
    created               = models.DateTimeField(auto_now_add=True)
    due_date              = models.DateField(auto_now=False, auto_now_add=False, null=True)
    last_edited           = models.DateTimeField(auto_now=True)
    last_accessed         = models.DateTimeField(auto_now=True)
    active                = models.BooleanField(default=True)

    #call the manager
    objects              = JobManager()

    class Meta:
        ordering         = ('-created', '-last_edited' )

    def __str__(self):
        return '%s %s' % (self.job_tittle, self.company)

    def __unicode__(self):
        return str(self.job_tittle)

    @classmethod
    def message(cls, today): pass
