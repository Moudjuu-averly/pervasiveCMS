# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from itertools import chain
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import ServiceForm, UpdateServiceForm
from services.models import Service
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

#Visitor
def view_all_services(request):
    services               = Service.objects.filter(active=True).filter(deleted=False).all()
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
        'services': services,
    }
    return render(request, 'pervasive/adclass/services/all_services.html', context )

#Visitor
def view_service(request, pk, slug):
    service = list()
    try:
        service               = get_object_or_404(Service, pk=pk, slug=slug)

        '''' Record the last accessed date and number of view'''
        service.last_accessed = timezone.now()
        '''model manager function with ip address META option'''
        view_by           = get_ip(request)
        qs                = service.objects.get(view_by__iexact=view_by).exist()
        if not qs:
        #increament service views
            service.update(views=F('views')+1)
            service.save()
        else: pass
    except: pass
    template_name = 'pervasive/adclass/services/single_service.html'
    context               = {
        'service'             : service,
    }
    return render(request, template_name, context)

def remote_service(request, location=None):
    service = list()
    try:
        service               = Service.objects.filter(active=True).filter(location='remote').all()
        '''model manager function with ip address META option'''
    except: pass
    template_name = 'services/adclass/service_filter.html'
    context = {
        'service': service,
    }

    return render(request, template_name, context)

def filter_service_type(request, service_type=None):
    service = list()
    try:
        service               = Service.objects.filter(service_type=service_type)
        '''' Record the last accessed date and number of view'''
        service.last_accessed = timezone.now()
        '''model manager function with ip address META option'''
        #service.increament
        service.last_accessed = timezone.now()
        service.save()
    except: pass
    context = {
        'service': service,
    }
    return render(request, 'services/adclass/service_filter.html', context)





'''
                                   For Clients(User)
                    The views below are indented to only be used by site
                            visitors that aren't logged in
'''

class ServiceView(TemplateView):
    template_name = 'profiles/adclass/services/all_services.html'

    def get(self, request, user =None):
        service                 = Service.objects.filter(user=request.user).filter(active=True).filter(deleted=False)
        context             = {
            "title": 'Services',
            'service': service,
        }
        return render(request, self.template_name, context)

'''
this line below are only views for the logged in user
'''
@login_required
def add_service(request):
    template_name = 'profiles/adclass/services/add_service.html'
    form = ServiceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('services:ServiceView')
        print(form.errors)
    else:
        form = ServiceForm(request.POST or None, request.FILES or None)

    context = {
        'form': form,
        "title": 'Services | add',
    }
    return render(request, template_name, context)


@require_http_methods(['GET'])
def search(request):
    query                               = request.GET.get('q')
    context                             = list()
    if query:
        object_list = Service.objects.active().filter(
                Q(service_icontains         = query)|
                Q(country__icontains    = query) |
                Q(city__icontains       = query)|
                Q(user__icontains       = query)|
                Q(service_type__icontains   = query)
                ).distinct().order_by('-created')
        template_name = 'profiles/adclass/services/service_search.html'
        context                         ={
            'object_list': object_list,
            'query': query
        }
        return render(request, template_name, context)
    return HttpResponse('Please type something.')

@login_required
def corp_all_service_view(request):
    service                 = Service.objects.active()
    template_name = 'profiles/adclass/services/all_services.html'
    context = {
        'service': service,
        'title': 'services',
    }
    return render(request, template_name, context)

@login_required
def corp_single_service_view(request, slug=None):
    service                 = get_object_or_404(Service, slug=slug)
    template_name       = 'profiles/adclass/services/single_service_corp.html'
    context = {
        'service': service,
    }
    return render(request, template_name, context)

@login_required
def delete_service(request, slug=None):
    service             = get_object_or_404(Service, slug=slug)
    service.deleted     = True
    service.active      = False
    service.save()
    return redirect("services:ServiceView")

@login_required
def restore_service(request, slug=None):
    service             = get_object_or_404(Service, slug=slug)
    service.deleted     = False
    service.active      = True
    service.save()
    return redirect("services:ServiceView")

@login_required
def delete_service_permanent(request, slug=None):
    service = get_object_or_404(Service, slug=slug)
    service.delete()
    service.save()
    return redirect("services:ServiceView")

@login_required
def update_service(request, slug=None):
    service = get_object_or_404(Service, slug=slug)
    template_name = 'profiles/adclass/services/edit_service.html'
    form = UpdateServiceForm(request.POST or None, request.FILES or None, instance=service)
    if form.is_valid():
        service = form.save(commit=False)
        service.edited = True
        service.last_edited = timezone.now()
        service.save()
        #messages.success(request, 'The service was successfully updated!')
        return redirect(reverse('services:corp_single_service_view', kwargs={'slug': service.slug}))
    else:
        form = UpdateServiceForm(request.POST or None, request.FILES or None, instance=service)
        #messages.error(request, 'Please the correct errors below!')

    context = {
    "title": service.service_tittle,
    "service": service,
    "form":form,
    }
    return render(request, template_name, context)
