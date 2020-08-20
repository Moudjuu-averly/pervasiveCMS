# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone
from itertools import chain
from django.views.generic import ListView
#from blog.models import Post
from flock.models import Post
from jobs.models import PostJob
from profiles.models import Profile
from services.models import Service
from products.models import Product
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods
#from events.models import Event

'''
This is the main site search view
'''

@require_http_methods(['GET'])
def search1(request):
    query = request.GET.get('q')
    if query:
        object_list = Post.objects.search()
        context={
            'object_list': object_list,
            'query': query
        }
        return render(request, 'flock/search_results.html', context)

class SearchView(ListView):
    template_name = 'pervasive/search/view.html'
    paginate_by = 20
    count = 0

    @require_http_methods(['GET'])
    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

@require_http_methods(['GET'])
def search(request):
    template_name = 'pervasive/search/view.html'
    query = request.GET.get('q')
    if query:
        flock_results = Post.objects.search()
        
        queryset_chain              = chain(
                flock_results,
                #job_results,
                #profile_results,
                #products_results,
                #services_results,
                #tenders_results
        )
        qs                           = sorted(queryset_chain,
            key                     = lambda instance: instance.pk,
            reverse                 = True #, klass = instance.__class__.__name__
            )
        #qs.count                  = len(qs)
        context={
            'object_list': qs,
            'query': query
        }
        return render(request, template_name, context)
    return HttpResponse('Please type something.')
