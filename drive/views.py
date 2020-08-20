# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from itertools import chain
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls import reverse
from adclass.models import TenderApplicant, Tender, Scholarship, Announce
from services.models import Service
from products.models import Product
from jobs.models import PostJob
from django.utils import timezone

def get_ip(request):
    try:
        x_foward = request.META.get("HTTP_X_FOWARDED_FOR")
        if x_foward:
            ip = x_foward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = '127.0.0.1'
    return ip


'''For Clients(User)'''
@login_required
def drive_main_view(request, user =None):
    template_name                   = 'profiles/drive/main_view.html'
    service_video = set()
    product_video = set()
    tender_video = set()
    job_video = set()
    announce_image = set()
    services                    = Service.objects.filter(user=request.user).filter(service_video=service_video).first()
    products                    = Product.objects.filter(user=request.user).filter(product_video=product_video).all()
    tenders                     = Tender.objects.filter(user=request.user).filter(tender_video=tender_video).all()
    jobs                        = PostJob.objects.filter(user=request.user).filter(job_video=job_video).all()
    announce                    = Announce.objects.filter(user=request.user).filter(announce_image=announce_image).all()
    #t_services                  = services.count()
    #t_products                  = products.count()
    #t_tenders                   = tenders.count()
    #t_jobs                      = jobs.count()
    #t_announce                  = announce.count()
    #total                       = t_services + t_products + t_tenders + t_jobs + t_announce
    context = {
        "title"                 : 'BC Drive | all files',
        'services'              : services,
        'products'              : products,
        'tenders'               : tenders,
        'jobs'                  : jobs,
        'announce'              : announce,
        #'total'                 : total,
    }
    return render(request, template_name, context)
