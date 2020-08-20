# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from flock.models import Post, Friend, Comments

class StarterPackageListView(ListView):
    """Package List View."""



class StarterPackageDetailView(DetailView):
    """Package Detail View."""



def choose_package(request):
    return render(request, 'finance/pay.html')
