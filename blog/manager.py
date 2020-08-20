# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import timedelta, time
from django.utils import timezone
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField


class BlogPostQuerySet(models.QuerySet):
#    def smaller_than(self, size):
#        return self.filter(size__lt=size)

#    def active(self):
#        return self.filter(active=True)
    def full_time(self):
        return self.filter(job_type='F')

    def part_time(self):
        return self.filter(job_type='P')

    def contract(self):
        return self.filter(job_type='C')

    def freelancer(self):
        return self.filter(job_type='L')

    def internship(self):
        return self.filter(job_type='I')

    def volunteer(self):
        return self.filter(job_type='V')

    def profileslug(self):
        #slug = slugify(instance.title)
        return slugify(self.job_tittle)

    #def trending(self, num = 3):
    #    return sefl.filter(rate__gt=num)


class BlogPostManager(models.Manager):
    """docstring for JobManager."""
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(blog_tittle__icontains=query) |
                         # Q(category__icontains=query)|
                         Q(content__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

    def get_queryset(self):
        return BlogPostQuerySet(self.model, using=self._db)  # Important!

    def save(self, *args, **kwargs):
        self.slug = slugify(self.blog_tittle)
        super(Tender, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('adclass.views.view_tender', args=[str(self.pk)])

    def tender_owner(self):
        return reverse('profiles:view_profile_with_pk', args=[str(self.user_id)])

    def type_filter(self):
        return reverse('adclass:filter_tender_type', args=[str(self.tender_type)])

    @property
    def type(self):
        return self.get_tender_type_display()

    @property
    def total_jobs(self):
        pass
        #return self.pk.count()
        #all = self.exclude(active=True).count()
        #return all

    def number_of_views(self):
        # Call the superclass
        object = super().number_of_views()
        # Record the last accessed date and increament number of job views
        object.last_accessed = timezone.now()
        object.num_of_views  = self.num_of_views + 1
        object.save()
        # Return the object
        return num_of_views

    def all_jobs(self):
        all_jobs            = self.objects.filter(active=True).all().order_by('-created')
        total_jobs          = self.objects.filter(active=True).count()
        owner_total         = self.objects.filter(active=True, args=[str(self.user.pk)]).count()
        type_total          = self.objects.filter(active=True, args=[str(self.job_type)]).count()
        if self.salary_scale is not None:
            scale           = self.salary_scale
        elif not self.salary_scale:
            scale           = self.min_salary * 12
            if self.max_salary and self.min_salary:
                scale       = ((self.max_salary * 12) - scale) / 12
        average_salary      = self.objects.aggregate(Avg(scale))
        top_paid_job        = self.objects.aggregate(Max(max_salary))

        '''
        Admin queries only
        '''
        quarter_total       = super().active().filter(created__quarter=2).count()
        mon_friday_jobs     = self.objects.filter(created__week_day__gte=2, created__week_day__lte=6).count()
        weekend_jobs        = self.objects.filter(created__week_day__gte=6, created__week_day__lte=2).count()

        def average(request):
            all_average     = self.objects.filter(active=True).aggregate(Avg('job_type'))
            all_type = self.objects.filter(active=True, args=[str(self.job_type)]).aggregate(Avg('job_type'))

        def top_jobs(request):
            above_3         = Count('postjob', filter=Q(postjob__rating__gt=3))
            below_4         = Count('postjob', filter=Q(postjob__rating__lte=4))
            _all            = super().active().annotate(below_4=below_4).annotate(above_3=above_3)
            _top_job        = super().active().all().aggregate(Max('rating'))
            low_rate        = _all[0].above_3
            top_rate        = _all[0].below_4
        return

    def edit_job(self):
        tender = Tender.objects.update(args=[str(self.id)])
        return reverse('adclass:update_tender', tender)
