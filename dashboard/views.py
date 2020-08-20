# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def dashboard_view(request):
    context = {

    }
    return render(request, 'dashboard/profile/view.html', {})
