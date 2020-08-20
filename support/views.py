# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from .models import Support
from .forms import SupportForm

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
def support_view(request):
    support = ''
    try:
        support                = Support.objects.filter(user=request.user).all()
    except Exception as e:
        pass
    context                 = {
    'tittle'                : 'Suppot | view',
    'support'                  : support,
     }
    return render(request, 'profiles/support/main_view.html', context)

@login_required
def contact_support(request):
    support = ''
    try:
        support                = Support.objects.get_or_create(user=request.user)
    except Exception as e:
        pass
    if request.method       == 'POST':
        form                = SupportForm(request.POST or None,  request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.seen_by_us = request.user
            instance.save()
            return redirect(reverse('support:support_view'))
        print(form.errors)
    else:
        form                = SupportForm(instance=request.user)
        context             = {
        'tittle'            : 'Suppot | Create',
        'form'              : form,
        'support'              : support,
         }
        return render(request, 'profiles/support/contact_support.html', context)
    return HttpResponseRedirect(reverse('support:support_view'))
