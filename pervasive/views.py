# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from finance.models import UserMembership, Membership
from profiles.models import Profile
from flock.models import Friend, Post, Comments
from jobs.models import PostJob
from products.models import Product
from services.models import Service
from adclass.models import Tender
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from newsletter.forms import JoinForm
from datetime import datetime
from itertools import chain
import json
from django.shortcuts import *
from django.template import RequestContext

                ###############################
                ###PERVASIVE HOME PAGE VIEW###
                ###############################

'''
Get the users ip address as the page loads to inrease relativity.
By means of viewing profiles by near location
'''
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

def near_by_loc(request):
    pass

'''
Page loads
'''
def pervasive_view(request):
    visitor_location    = get_ip(request)
    #visits = VsitForm(request.POST or None)
    #relate = User.BusinessBaseProfile.near_by('user_location').all().order_by('ip_address')
    profile                     = Profile.objects.filter(active=True).all()


    '''
    basecode newsletter subscription form
    '''
    # join_form = JoinForm(request.POST or None)
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     response_data = {}
    #     #join_form = JoinForm(email = email)
    #     join_form.save(commit=False)
    #     join_form.ip_address = get_ip(request)
    #     join_form.save()
    #
    #     response_data['result'] = 'Success!!.'
    #
    #     return HttpResponse(
    #         json.dumps({response_data}),
    #         content_type="application/json"
    #     )
    # else:
    #     return HttpResponse(
    #         json.dumps({"nothing to see": "this isn't happening"}),
    #         content_type="application/json"
    #     )
    join_form = JoinForm(request.POST or None)
    if join_form.is_valid():
        join_form.save(commit=False)
        join_form.ip_address = get_ip(request)
        join_form.save()
        return redirect(reverse('pervasive:HomeView'))
    ''''''
    tittle = 'Pervasive | home'
    context = {
        'tittle'        : tittle,
        'join_form'     : join_form,
        'profile'       : profile,
    }
    return render(request, 'pervasive/home/home.html', context)

def product_n_services(request):
    template_name = 'pervasive/ps/product_n_services.html'
    products_results                = Product.objects.all()
    services_results                = Service.objects.all()
    tenders_results                 = Tender.objects.all()

    queryset_chain              = chain(
            products_results,
            services_results,
            tenders_results
    )
    qs                           = sorted(queryset_chain,
        key                     = lambda instance: instance.created or instance.created,
        reverse                 = True
        )
    #qs.count                  = len(qs)
    context={
        'object_list': qs,
    }
    return render(request, template_name, context)

def validate_email(request):
    email = request.GET.get('email', None)
    data = {
        'is_taken': JoinForm.objects.filter(email__iexact=email__iexact).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)
