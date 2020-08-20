# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from itertools import chain
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls import reverse
from adclass.forms import TenderForm, TenderApplicantForm, ScholarshipForm, AnnounceForm, EditTenderForm
from . models import TenderApplicant, Tender, Scholarship, Announce
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
class AdClassView(TemplateView):
    template_name                   = 'profiles/adclass/main_view.html'
    def get(self, request, user =None):
        services                    = Service.objects.filter(user=request.user).filter(active=True).filter(deleted=False).all()
        products                    = Product.objects.filter(user=request.user).filter(active=True).filter(deleted=False).all()
        tenders                     = Tender.objects.filter(user=request.user).filter(active=True).filter(deleted=False).all()
        jobs                        = PostJob.objects.filter(user=request.user).filter(active=True).filter(deleted=False).all()
        announce                    = Announce.objects.filter(user=request.user).filter(active=True).filter(deleted=False).all()
        t_services                  = services.count()
        t_products                  = products.count()
        t_tenders                   = tenders.count()
        t_jobs                      = jobs.count()
        t_announce                  = announce.count()
        total                       = t_services + t_products + t_tenders + t_jobs + t_announce
        context = {
            "title"                 : 'ads | manager',
            'services'              : services,
            'products'              : products,
            'tenders'               : tenders,
            'jobs'                  : jobs,
            'announce'              : announce,
            'total'                 : total,
        }
        return render(request, self.template_name, context)

@login_required
def add_tender(request):
    template_name = 'profiles/adclass/tender/add_tender.html'
    form = TenderForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        tender = form.save(commit=False)
        tender.user = request.user
        tender.save()
        return redirect('adclass:AdClassView')
    else:
        form = TenderForm(request.POST or None, request.FILES or None)
    #print(form.errors)
    context = {
        'tiltte': 'Tender | add',
        'form': form,
    }
    return render(request, template_name, context)

@login_required
def corp_all_tender_view(request):
    tenders                 = Tender.objects.filter(user=request.user).order_by('-created')
    template_name       = 'profiles/adclass/tender/all_tenders.html'
    context             = {
        'tittle': 'Tenders | all',
        'tenders': tenders,
    }
    return render(request, template_name, context)

@login_required
def corp_single_tender_view(request, slug=None):
    tender                 = get_object_or_404(Tender, slug=slug)
    template_name = 'profiles/adclass/tender/single_tender.html'
    context = {
        'title': 'Tender | All',
        'tender': tender,
    }
    return render(request, template_name, context)

@login_required
def update_tender(request, slug=None):
    tender = get_object_or_404(Tender, slug=slug)
    template_name = 'profiles/adclass/tender/update_tender.html'
    form = EditTenderForm(request.POST or None, request.FILES or None, instance=tender)
    if form.is_valid():
        tender          = form.save(commit=False)
        tender.edited   = True
        tender.updated  = timezone.now()
        tender.save()
        return redirect(reverse('adclass:corp_single_tender_view', kwargs={'slug': tender.slug}))
    else:
        form = EditTenderForm(request.POST or None, request.FILES or None, instance=tender)
        #messages.success(request, 'Your password was updated successfully!')
    context = {
        'title': 'Tender | update',
        "tender": tender,
        "form":form,
    }
    return render(request, template_name, context)

@login_required
def delete_tender(request, slug=None):
    tender             = get_object_or_404(Tender, slug=slug)
    tender.deleted     = True
    tender.active      = False
    tender.save()
    return redirect("adclass:AdClassView")

@login_required
def restore_tender(request, slug=None):
    tender             = get_object_or_404(Tender, slug=slug)
    tender.deleted     = False
    tender.active      = True
    tender.save()
    return redirect("adclass:AdClassView")

@login_required
def delete_tender_permanent(request, slug=None):
    tender = get_object_or_404(Tender, slug=slug)
    tender.delete()
    tender.save()
    return redirect("adclass:AdClassView")


'''
ANNOUNCEMTNTS
'''
@login_required
def add_announce(request):
    template_name = 'profiles/adclass/general/add_announce.html'
    form = AnnounceForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        announce = form.save(commit=False)
        announce.user = request.user
        announce.save()
        return redirect('adclass:AdClassView')
    else:
        form = AnnounceForm(request.POST or None, request.FILES or None)
    #print(form.errors)
    context = {
        'tittle': 'Announcements | add',
        'form': form,
    }

    return render(request, template_name, context)

@login_required
def corp_all_announce_view(request):
    announce                 = Announce.objects.filter(user=request.user).order_by('-created')
    template_name       = 'profiles/adclass/general/all_announcements.html'
    context             = {
        'title': 'Announcements | all',
        'announce': announce,
    }
    return render(request, template_name, context)

@login_required
def corp_single_announce_view(request, slug=None):
    announce                 = get_object_or_404(Announce, slug=slug)
    template_name = 'profiles/adclass/general/single_announce_corp.html'
    context = {
        'title': 'Announcement',
        'announce': announce,
    }
    return render(request, template_name, context)

@login_required
def delete_announce(request, slug=None):
    announce             = get_object_or_404(Announce, slug=slug)
    announce.deleted     = True
    announce.active      = False
    announce.save()
    return redirect("adclass:AdClassView")

@login_required
def restore_tender(request, slug=None):
    announce             = get_object_or_404(Announce, slug=slug)
    announce.deleted     = False
    announce.active      = True
    announce.save()
    return redirect("adclass:AdClassView")

@login_required
def delete_tender_permanent(request, slug=None):
    announce = get_object_or_404(Announce, slug=slug)
    announce.delete()
    announce.save()
    return redirect("adclass:AdClassView")





#Visitor
def view_all_tenders(request):
    tenders = list()
    try:
        tenders               = Tender.objects.filter(active=True).filter(deleted=False).all()
    except: pass

    paginator = Paginator(tenders, 2) # Show 25 jobs per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        tenders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tenders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tenders = paginator.page(paginator.num_pages)
    #template_name
    context = {
        'tenders': tenders,
    }
    return render(request, 'adclass/all_tenders.html', {'tenders': tenders,})


def view_tender(request, slug=None):
    template_name = 'pervasive/adclass/tender/single_tender.html'
    tender = list()
    try:
        tender               = get_object_or_404(Tender, slug=slug)
        ''''
        Record the last accessed date and number of view
        model manager function with ip address META PARAM option
        '''
        view_by           = get_ip(request)
        qs                = tender.objects.get(view_by__iexact=view_by).exist()
        if not qs:
            '''increament tender views by one(Only if the user has not viewed before)'''
            tender.update(views=F('views')+1)
            tender.view_by = get_ip(request)
            tender.save()
        else: pass
        tender.views = views + 1
        #tender.last_accessed = timezone.now()
        tender.save()
    except: pass
    context = {
        'tender': tender,
    }
    return render(request, template_name, context)

def filter_tender_type(request, tender_type=None):
    tender = list()
    try:
        tender               = Tender.objects.filter(tender_type=tender_type)
    except:
        pass
    template_name = 'profiles/adclass/tenders/tender_filter.html'
    context = {
        'tittle': tender.tender_type,
        'tender': tender,
    }
    return render(request, template_name, context)

@require_http_methods(['GET'])
def search(request):
    query                               = request.GET.get('q')
    context                             = list()
    if query:
        object_list = Tender.objects.all().filter(
                Q(job_icontains         =query)|
                Q(country__icontains    =query) |
                Q(city__icontains       =query)|
                Q(user__icontains       =query)|
                Q(job_type__icontains   =query)
                ).distinct().order_by('-created')
        context                         ={
            'object_list': object_list,
            'query': query
        }
        return render(request, 'jobs/job_search.html', context)
    return HttpResponse('Please type something.')
