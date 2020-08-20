# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from newsletter.forms import ContactForm
from newsletter.models import Contact

def plans(request):
    template = 'pervasive/about/about.html'
    form = ContactForm()
    #def post(request, *args, **kwargs):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        if request.is_ajax():
            error = None
            success = None
            try:
                new_request = form.objects.create_request(
                                    request.POST['email'],request.POST['full_name'],email,request.POST['subject'],request.POST['message'])

                new_request.save()
                success = 'Ok'
            except Exception as e:
                error = CONTACT_FORM_ERROR

            if error :
                return HttpResponse(error)
            else:
                return HttpResponse(success)
    else:
        form = ContactForm(request.POST or None)
        #print(new_request.error)
    context = {
        'form': form,
    }
    return render(request, template, context )

@login_required
def upgrade(request):
    template = 'profiles/about/upgrade.html'
    context = {
        'tittle': 'Plans | upgrade',
    }
    return render(request, template, context )

def testimonies(request):
    template = 'pervasive/about/testimonies.html'
    #context = {
    #    'job': job,
    #}
    return render(request, template, {})

def our_team(request):
    template = 'pervasive/about/our_team.html'
    #context = {
    #    'job': job,
    #}
    return render(request, template, {})

def faqs(request):
    template = 'pervasive/about/faqs/all_faqs.html'
    #context = {
    #    'job': job,
    #}
    return render(request, template, {})
