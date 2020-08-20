# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import (
    RegistrationForm,
    EditProfileForm,
    EditPervasive
)
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from flock.models import Friend, Post, Comments
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from finance.models import *
from newsletter.forms import JoinForm
from profiles.forms import (
    EditDisplay, EditContact, EditMedia, ProfileImageForm,
    ProfileCoverImageForm, ProfileAboutVideoForm, ProfileWhoWeAreVideoForm,
    ProfileServicesVideoForm, ProfileProjectsVideoForm )
from profiles.models import Profile
from newsletter.models import Join
from jobs.models import PostJob

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


def register(request):
    if request.method =='POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('flock:HomeView'))
    else:
        form = RegistrationForm()
        context = {'form': form}
        return render(request, 'accounts/register.html', context)
    return HttpResponseRedirect(reverse('accounts:register'))

def login(request):
    form = RegistrationForm()
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('flock:HomeView'))
    else:
        form = RegistrationForm()
        # context = {'form': form}
        context = {}
        return render(request, 'accounts/login.html', context)
    return HttpResponseRedirect(reverse('accounts:login'))

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = User.authenticate(request, username=username, password=password)
#         #request.session.flush()
#         if user is not None and user.is_active:
#             login(request, user)
#             return HttpResponseRedirect(reverse('flock:HomeView'))
#         else:
#             # Return an 'invalid login' error message.
#             return render(request, 'accounts/login.html')
#     else:
#         return HttpResponseRedirect('Invalid username or password')
#
#     #return HttpResponseRedirect(reverse('accounts:login'))

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)

        context = {'form': form}
        return render(request, 'profiles/edit/change_password.html', context)

@login_required
def view_profile(request, pk=None):
    from profiles.models import Profile
    if pk:
        user            = user.objects.get(pk=pk)
    else:
        user            = user.objects.get(pk=request.user.pk)
    context             = { 'profile': profile, }
    return render(request, 'profiles/view/view_profile.html', context)

@login_required
def edit_profile(request):
    user            = User.objects.filter(pk=request.user.pk)
    context = {}
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.ip_address         = get_ip(request)
            form.save()
            return HttpResponseRedirect(reverse('accounts:view_profile'))
    else:
        form = EditProfileForm(instance=request.user)
        context = {'form': form}
        return render(request, 'profiles/edit/edit_admin_info.html', context)

@login_required
def edit_view(request):
    context = { 'title':'Profile | edit' }
    return render(request, 'profiles/edit/edit_view.html', context)

@login_required
def edit_display(request):
    profile                 = Profile.objects.get_or_create(user=request.user)
    if request.method       == 'POST':
        form                = EditDisplay(request.POST,  instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:edit_view'))
    else:
        form                = EditDisplay(instance=request.user.profile)
        context             = {
        'title'              : 'Edit display',
        'form'              : form,
        'profile'           : profile,
         }
        return render(request, 'profiles/edit/display/update.html', context)

    return HttpResponseRedirect(reverse('accounts:edit_view'))

@login_required
def edit_contacts(request):
    profile                 = Profile.objects.get_or_create(user=request.user)
    if request.method       == 'POST':
        form                = EditContact(request.POST,  instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:edit_view'))
    else:
        form                = EditContact(instance=request.user.profile)
        context             = {
        'title'              : 'Edit contacts',
        'form'              : form,
        'profile'           : profile,
         }
        return render(request, 'profiles/edit/contacts/update.html', context)

    return HttpResponseRedirect(reverse('accounts:edit_view'))

@login_required
def edit_media(request):
    profile = Profile.objects.get_or_create(user=request.user)
    context = {
    profile: profile,
    'title':'Profile | edit-media',
     }
    return render(request, 'profiles/edit/media/media_edit_view.html', context)

@login_required
def edit_profile_image(request):
    template_name           ='profiles/edit/media/profile_image.html'
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method       == 'POST':
        form                = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:edit_view'))
        print(form.errors)
    else:
        form                = ProfileImageForm(instance=request.user.profile)
    #template_name = form.template_name
    context = {
    'profile': profile,
    'form': form,
    'title':'Profile | image',
     }
    return render(request, template_name, context)


@login_required
def edit_cover_image(request):
    template_name           ='profiles/edit/media/cover_image.html'
    profile = Profile.objects.get_or_create(user=request.user)
    if request.method       == 'POST':
        form                = ProfileCoverImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:edit_view'))
        print(form.errors)
    else:
        form                = ProfileCoverImageForm(instance=request.user.profile)
    #template_name = form.template_name
    context = {
    'profile': profile,
    'form': form,
    'title':'Cover | image',
     }
    return render(request, template_name, context)
