from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from django.shortcuts import render, get_object_or_404, redirect


class ProfileQuerySet(models.QuerySet):
#    def smaller_than(self, size):
#        return self.filter(size__lt=size)

    def active(self):
        return self.filter(active=True)

    def regular(self):
        return self.filter(account_type='R')

    def gold(self):
        return self.filter(account_type='G')

    def platinum(self):
        return self.filter(account_type='P')

    def profileslug(self):
        #slug = slugify(instance.title)
        return slugify(self.user)

    def top_rated(self, num = 3):
        return self.filter(rate__gt=num)

class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)  # Important!

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user)
        super(Profile, self).save(*args, **kwargs)

    def active(self):
        return self.get_queryset().active()

    def regular(self):
        return self.get_queryset().regular()

    def gold(self):
        return self.get_queryset().gold()

    def platinum(self):
        return self.get_queryset().platinum()

    def profileslug(self):
        return self.get_queryset().profileslug()

    def top_rated(self):
        return self.get_queryset().top_rated()

    def get_absolute_url(self):
        from django.urls import reverse
        return HttpResponseRedirect(reverse('profiles:view_profile_visitor', kwargs=[str(self.slug)]))

    @property
    def type(self):
        return self.get_business_type_display()

    @property
    def regular_sum(self):
        return self.objects.aggregate(regular=Count('pk', filter=Q(account_type=Client.REGULAR)))

    def owner(self):
        from django.urls import reverse
        return reverse('profiles:view_profile_with_pk', args=[str(self.user.pk)])

    @property
    def calculate_prices(self):
        all_costs = self.product.products.all() #products comes from related name of a foreign key field
        price_list = [x.cost for x in all_costs]
        add_price = sum(price_list)
        if add_price >= self.budget:
            return "You're in danger of overspending my friend"
        elif add_price <= self.budget:
            calc_budget = self.budget - add_price
            return "You are under budget with ${} left over".format(calc_budget)
        else:
            return "Cannot Compute, please add in a budget and/or product prices."

    #def active(self, *args, **kwargs):
    #    qs = self.get_queryset().filter(
    #                        draft=False,
    #                        publish__lte=timezone.now()
    #                        )
    #    return qs

    def all_profiles(self):
        all_jobs            = self.objects.filter(active=True).all().order_by('-created')
        jobs_total          = self.objects.filter(active=True).count()
        owner_total         = self.objects.filter(active=True, args=[str(self.user.pk)]).count()
        type_total          = self.objects.filter(active=True, args=[str(self.job_type)]).count()

        def average(request):
            all_average     = self.objects.filter(active=True).all().aggregate(Avg('job_type'))
            all_type        = self.objects.filter(active=True, args=[str(self.job_type)]).aggregate(Avg('job_type'))

        def top_jobs(request):
            above_3         = Count('postjob', filter=Q(postjob__rating__gt=3))
            below_4         = Count('postjob', filter=Q(postjob__rating__lte=4))
            all_job_rates   = super().active().annotate(below_4=below_4).annotate(above_3=above_3)
            top_job         = super().active().all().aggregate(Max('rating'))
            low_rate        = all_job_rates[0].above_3
            top_rate        = all_job_rates[0].below_4
        return

    def edit_job(self):
        job = PostJob.objects.update(args=[str(self.id)])
        return reverse('jobs:view_all_jobs', job)


    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(about__icontains=query)|
                    Q(country_origin__icontains=query) |
                    Q(country_city__icontains=query) |
                    Q(address__icontains=query) |
                    Q(website__icontains=query) |
                    Q(other_website__icontains=query) |
                    Q(blog__icontains=query) |
                    Q(other_names__icontains=query) |
                    Q(official_business_name__icontains=query)
                          )
            query = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return query

    def upload_location(instance, filename):
        ProfileModel = instance.__class__
        new_id = ProfileModel.objects.order_by("id").last().id + 1
        return "%s/%s" %(new_id, filename)

    def get_like_url(self):
        pass
        #return reverse("flock:like-toggle", kwargs={"slug": self.slug})

    def get_api_like_url(self):
        pass
        #return reverse("flock:like-api-toggle", kwargs={"slug": self.slug})

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @property
    def video_url(self):
        if self.about_video and hasattr(self.video, 'url'):
            return self.about_video.url
