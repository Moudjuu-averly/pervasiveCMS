# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from flock.models import Friend, Post, Comments
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user_model
from finance.models import *
from profiles.models import Profile
from newsletter.forms import JoinForm
from newsletter.models import Join
from django.contrib.auth.models import User
from flock.models import Post

@login_required
def view_profile(request, slug=None, user=None):
    user                = Profile.objects.filter(slug=slug).filter(user=request.user)
    context             = {
    'user': user,
    }
    return render(request, 'profiles/view/view_profile.html', context)

def view_profile_visitor(request, slug=None):
    business_type           = set()
    profile                 = Profile.objects.filter(slug=slug).filter(active=True).select_related('user').all()
    #related_profiles        = Profile.objects.filter(business_type=profile.business_type).filter(active=True).exclude(pk=profile.pk).all()
    context                 = {
    'tittle'                : 'Profile',
    'profile'               : profile,
    #'related_profiles'      : related_profiles,
    }
    return render(request, 'pervasive/profiles/base_profile.html', context)

def single_post(request, slug=None):
    template_name = 'pervasive/posts/single_post.html'
    post          = list()
    related_posts = list()
    try: 
        post               = get_object_or_404(Post, slug=slug)
        related_posts      = Post.objects.filter(category=post.category).filter(deleted=False).exclude(pk=blog.pk).all()
        ''''
        Record the last accessed date and number of view
        model manager function with ip address META PARAM option
        '''
        view_by           = get_ip(request)
        qs                = post.objects.get(view_by__iexact=view_by).exist()
        if not qs:
            '''increament blog views by one(Only if the user has not viewed before)'''
            post.update(views=F('views')+1)
            post.view_by = get_ip(request)
            post.save()
        else: pass
        post.views = views + 1
        post.last_accessed = timezone.now()
        post.save()
    except: pass
    context = {
        "title"        : 'Blog | view',
        'post'         : post,
        'related_posts': related_posts,
    }
    return render(request, template_name, context)
