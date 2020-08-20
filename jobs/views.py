# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
from .forms import JobForm, UpdateJobForm
from jobs.models import PostJob, RePostJob
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from . stream import stream_video
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



'''
                                   For Clients(User)
                    The views below are indented to only be used by site
                            visitors that aren't logged in
'''

#Visitor
def view_all_jobs(request):
    jobs_results                = PostJob.objects.filter(active=True).filter(deleted=False).all()
    re_jobs_results             = RePostJob.objects.filter(active=True).filter(deleted=False).all()
    queryset_chain              = chain(
             jobs_results,
             re_jobs_results,
    )
    qs                          = sorted(queryset_chain,
        key                     = lambda instance: instance.created or instance.created,
        reverse                 = True
        )
     #qs.count                  = len(qs)
    paginator = Paginator(qs, 15) # Show 25 jobs per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qs = paginator.page(paginator.num_pages)

    context = {
        'object_list': qs,
    }
    return render(request, 'pervasive/jobs/all_jobs.html', context )

#Visitor
def view_job(request, pk, slug):
    job = list()
    try:
        job               = get_object_or_404(PostJob, pk=pk, slug=slug)
        related_job        = PostJob.objects.filter(active=True).filter(deleted=False).filter(job_type=job.job_type).all()

        '''' Record the last accessed date and number of view'''
        job.last_accessed = timezone.now()
        '''model manager function with ip address META option'''
        view_by           = get_ip(request)
        qs                = job.objects.filter(view_by__iexact=view_by).exist()
        if not qs:
        #increament job views
            job.views = F('views') + 1
            #job.update(views=F('views')+1)
            job.save()
        else: pass
        print(view_by)
    except: pass
    template_name = 'pervasive/jobs/single_job.html'
    context               = {
        'title'             : 'Job | view',
        'job'             : job,
        'related_job'             : related_job,
    }
    return render(request, template_name, context)

def remote_jobs(request):
    template_name = 'pervasive/jobs/remote_jobs.html'

    jobs_results                = PostJob.objects.filter(active=True).filter(deleted=False).filter(location='R').all()
    re_jobs_results             = RePostJob.objects.filter(active=True).filter(deleted=False).filter(location='R').all()
    queryset_chain              = chain(
             jobs_results,
             re_jobs_results,
    )
    qs                          = sorted(queryset_chain,
        key                     = lambda instance: instance.created or instance.created,
        reverse                 = True
        )

    paginator = Paginator(qs, 15) # Show 25 jobs per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        qs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        qs = paginator.page(paginator.num_pages)

    context = {
        'title'             : 'Jobs | remote',
        'object_list': qs,
    }

    return render(request, template_name, context)

def filter_job_type(request, job_type=None):
    job = list()
    try:
        job               = PostJob.objects.filter(job_type=job_type)
        '''' Record the last accessed date and number of view'''
        job.last_accessed = timezone.now()
        '''model manager function with ip address META option'''
        #job.increament
        job.last_accessed = timezone.now()
        job.save()
    except: pass
    context = {
        'job': job,
    }
    return render(request, 'jobs/job_filter.html', context)





'''
This VIEWS below are only views for the logged in user
'''

class JobView(TemplateView):
    template_name = 'profiles/jobs/all_jobs.html'

    #form = JobForm()
    def get(self, request, user =None):
        form                = JobForm()
        job                 = PostJob.objects.filter(user=request.user).filter(active=True).filter(deleted=False)

        context             = {
            'form': form,
            #"title": '{{user|capfirst - }}Jobs',
            'job': job,
        }
        return render(request, self.template_name, context)


@login_required
def add_job(request):
    template_name = 'profiles/jobs/add_job.html'
    form = JobForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('jobs:JobView')
    #print(form.errors)
    else:
        form = JobForm(request.POST or None, request.FILES or None)

    context = {
        'form': form,
        "title": 'Jobs | add',
    }
    return render(request, template_name, context)


@require_http_methods(['GET'])
def search(request):
    query                               = request.GET.get('q')
    context                             = list()
    if query:
        object_list = PostJob.objects.active().filter(
                Q(job_icontains         = query)|
                Q(country__icontains    = query) |
                Q(city__icontains       = query)|
                Q(user__icontains       = query)|
                Q(job_type__icontains   = query)
                ).distinct().order_by('-created')
        template_name = 'jobs/job_search.html'
        context                         ={
            'object_list': object_list,
            'query': query
        }
        return render(request, template_name, context)
    return HttpResponse('Please type something.')

@login_required
def corp_all_job_view(request):
    job                 = PostJob.objects.active()
    template_name = 'profiles/jobs/all_jobs.html'
    context = {
        'job': job,
        'title': 'Jobs',
    }
    return render(request, template_name, context)

@login_required
def corp_single_job_view(request, slug=None):
    job                 = get_object_or_404(PostJob, slug=slug)
    template_name       = 'profiles/jobs/single_job_corp.html'
    context = {
        'job': job,
    }
    return render(request, template_name, context)

@login_required
def delete_job(request, slug=None):
    job             = get_object_or_404(PostJob, slug=slug)
    job.deleted     = True
    job.active      = False
    job.save()
    return redirect("jobs:JobView")

@login_required
def restore_job(request, slug=None):
    job             = get_object_or_404(PostJob, slug=slug)
    job.deleted     = False
    job.active      = True
    job.save()
    return redirect("jobs:JobView")

@login_required
def delete_job_permanent(request, slug=None):
    job = get_object_or_404(PostJob, slug=slug)
    job.delete()
    job.save()
    return redirect("jobs:JobView")

@login_required
def update_job(request, slug=None):
    job = get_object_or_404(PostJob, slug=slug)
    template_name = 'profiles/jobs/edit_job.html'
    form = UpdateJobForm(request.POST or None, request.FILES or None, instance=job)
    if form.is_valid():
        job = form.save(commit=False)
        job.edited = True
        job.last_edited = timezone.now()
        job.save()
        #messages.success(request, 'The job was successfully updated!')
        return redirect(reverse('jobs:corp_single_job_view', kwargs={'slug': job.slug}))
    else:
        form = UpdateJobForm(request.POST or None, request.FILES or None, instance=job)
        #messages.error(request, 'Please the correct errors below!')

        context = {
        "title": job.job_tittle,
        "job": job,
        "form":form,
    }
    return render(request, template_name, context)
