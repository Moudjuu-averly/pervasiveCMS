# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from itertools import chain
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls import reverse
from services.models import Service
from products.models import Product
from jobs.models import PostJob
from adclass.models import Tender
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_ip(request):
    try:
        x_foward = request.META.get("HTTP_X_FOWARDED_FOR")
        if x_foward:
            ip = x_foward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ''
    return ip

@login_required
def view_all_deleted(request):
    services                    = Service.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    products                    = Product.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    tenders                     = Tender.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    jobs                        = PostJob.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    t_products                  = products.count()
    t_tenders                   = tenders.count()
    t_services                  = services.count()
    t_jobs                      = jobs.count()
    total                       = t_services + t_products + t_tenders + t_jobs
    paginator = Paginator(services, 15) # Show 25 services per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        services = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        services = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        services = paginator.page(paginator.num_pages)

    context = {
        'title': 'Trashed | all',
        'services': services,
        'products': products,
        'tenders': tenders,
        'jobs': jobs,
        'total': total,
    }
    return render(request, 'profiles/recycle/all_deleted.html', context )

@login_required
def deleted_jobs(request):
    jobs                   = PostJob.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    context = {
        'title': 'Trashed | jobs',
        'jobs': jobs,
    }
    return render(request, 'profiles/recycle/deleted_jobs.html', context )

@login_required
def deleted_services(request):
    services                   = Service.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    context = {
        'title': 'Trashed | services',
        'services': services,
    }
    return render(request, 'profiles/recycle/services/deleted_services.html', context )

@login_required
def deleted_tenders(request):
    tenders                   = Tender.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    context = {
        'title': 'Trashed | tenders',
        'tenders': tenders,
    }
    return render(request, 'profiles/recycle/deleted_tenders.html', context )

@login_required
def deleted_products(request):
    products                   = Product.objects.filter(user=request.user).filter(active=True).filter(deleted=True).all()
    context = {
        'title': 'Trashed | products',
        'products': products,
    }
    return render(request, 'profiles/recycle/deleted_products.html', context )
