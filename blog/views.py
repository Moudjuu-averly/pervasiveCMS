# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
from blog.models import BlogPost
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

'''
Blog Posts Views
'''
def view_all_blogs(request):
    blogs = list()
    try:
        blogs                       = BlogPost.objects.filter(active=True).filter(deleted=False).all()
    except: pass

    paginator = Paginator(blogs, 2) # Show 25 jobs per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tenders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)
    template_name = 'pervasive/blog/all_blogs.html'

    context = {
        "title": 'Blog | all',
        'blogs': blogs,
    }
    return render(request, template_name, {'blogs': blogs,})


def single_blog(request, slug=None):
    template_name = 'pervasive/blog/single_blog.html'
    blog          = list()
    related_blogs = list()
    try:
        blog               = get_object_or_404(BlogPost, slug=slug)
        related_blogs      = BlogPost.objects.filter(blog_category=blog.blog_category).filter(deleted=False).exclude(pk=blog.pk).all()
        ''''
        Record the last accessed date and number of view
        model manager function with ip address META PARAM option
        '''
        view_by           = get_ip(request)
        qs                = blog.objects.get(view_by__iexact=view_by).exist()
        if not qs:
            '''increament blog views by one(Only if the user has not viewed before)'''
            blog.update(views=F('views')+1)
            blog.view_by = get_ip(request)
            blog.save()
        else: pass
        blog.views = views + 1
        blog.last_accessed = timezone.now()
        blog.save()
    except: pass
    context = {
        "title"        : 'Blog | view',
        'blog'         : blog,
        'related_blogs': related_blogs,
    }
    return render(request, template_name, context)


def view_all_news(request):
    news = list()
    try:
        news                       = BlogPost.objects.filter(active=True).filter(deleted=False).filter(blog_category='N').all()
    except: pass

    paginator = Paginator(news, 2) # Show 25 jobs per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = paginator.page(paginator.num_pages)
    template_name = 'pervasive/blog/all_blogs.html'

    context = {
        "title": 'News | all',
        'news': news,
    }
    return render(request, template_name, context )


def single_news(request, slug=None):
    template_name = 'pervasive/blog/single_blog.html'
    news          = list()
    related_news = list()
    try:
        news               = get_object_or_404(BlogPost, slug=slug)
        related_news      = BlogPost.objects.filter(blog_category=news.blog_category).filter(deleted=False).exclude(pk=news.pk).all()
        ''''
        Record the last accessed date and number of view
        model manager function with ip address META PARAM option
        '''
        view_by           = get_ip(request)
        qs                = news.objects.get(view_by__iexact=view_by).exist()
        if not qs:
            '''increament blog views by one(Only if the user has not viewed before)'''
            news.update(views=F('views')+1)
            news.view_by = get_ip(request)
            news.save()
        else: pass
        news.views = views + 1
        news.last_accessed = timezone.now()
        news.save()
    except: pass
    context = {
        "title"        : 'News | view',
        'news'         : news,
        'related_news': related_news,
    }
    return render(request, template_name, context)
