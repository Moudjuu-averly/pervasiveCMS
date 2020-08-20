# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from settings.forms import ChangeSettings

def index(request):
    # if request.method =='POST':
    #     form = ChangeSettings(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect(reverse('settings:update'))
    # else:
    #     form = ChangeSettings()
    #
    #     args = {'form': form}
    #     return render(request, 'settings/settings.html', args)

    #return HttpResponseRedirect(reverse('settings:update'))
    #return render(request, 'flock/post_detail.html')
    return render(request, 'settings/settings.html')
