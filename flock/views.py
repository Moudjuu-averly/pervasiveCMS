# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except:
    pass


from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from django.views.generic import TemplateView
from itertools import chain
from django.views.generic import ListView
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls import reverse
from flock.forms import HomeForm
from flock.models import Post, Friend, Comments
from jobs.models import PostJob
from profiles.models import Profile
from services.models import Service
from products.models import Product
from adclass.models import Tender
from blog.models import BlogPost


class HomeView(TemplateView):
    template_name = 'flock/post_detail.html'

    form = HomeForm()
    def get(self, request, pk =None):
        form = HomeForm()
        friends = list()
        comments = list()
        user = None
        try:
            instance = Post.objects.all().order_by('-timestamp')
            users = User.objects.exclude(id=request.user.id)
            user = User.objects.all()
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            likes = like.all()
            comments = Comments.objects.all().order_by('-timestamp')
            request.session.flush()
        except:
            pass

        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user

        context = {
            'form': form,
            'users': users,
            'user': user,
            'friends': friends,
            "title": 'flock | home',
            'instance': instance,
            'comments': comments,

        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = HomeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('flock:HomeView')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)



def view_single_flock(request, slug=None):
    try:
        flock = Post.objects.filter(slug=slug)
    except:
        pass

    context = {
        'flock': flock,
    }
    return render(request, 'pervasive/flock/single_flock.html', context)

def view_all_flocks(request):

        flocks                      = list()
        try:
            flocks                  = Post.objects.all()
        except:
            flocks                  = ''
        paginator                   = Paginator(flocks, 25) # Show 25 jobs per page
        page_request_var            = "page"
        page                        = request.GET.get(page_request_var)
        try:
            flocks                  = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            flocks                  = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            flocks                  = paginator.page(paginator.num_pages)

        context                     = {
            'flocks': flocks,
        }
        return render(request, 'pervasive/flock/all_flocks.html', context)


@require_http_methods(['GET'])
def search(request):
    template_name = 'pervasive/search/tabs/search_results.html'
    query = request.GET.get('q')
    if query:
        flock_results = Post.objects.search(query)
        job_results                     = PostJob.objects.search(query)
        blogpost_results                = BlogPost.objects.search(query)
        profile_results                 = Profile.objects.search(query)
        products_results                = Product.objects.search(query)
        services_results                = Service.objects.search(query)
        tenders_results                 = Tender.objects.search(query)

        queryset_chain              = chain(
                flock_results,
                job_results,
                profile_results,
                products_results,
                blogpost_results,
                tenders_results
        )
        qs                           = sorted(queryset_chain,
            key                     = lambda instance: instance.created or instance.created,
            reverse                 = True
            )
        #qs.count                  = len(qs)
        context={
            'object_list': qs,
            'query': query
        }
        return render(request, template_name, context)
    return HttpResponse('Please type something.')


class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        print(slug)
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return HttpResponseRedirect(reverse("flock:HomeView"))


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeAPIToggle(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug=None, format=None):
        # slug = self.kwargs.get("slug")
        obj = get_object_or_404(Post, slug=slug)
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False
        if user.is_authenticated():
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True
        data = {
            "updated": updated,
            "liked": liked
        }
        return HttpResponseRedirect(reverse("flock:HomeView"))

def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = HomeForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,
    }
    return render(request, "posts/post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    return redirect("flock:HomeView")


def change_friends(request, operation, pk):

    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)
    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('flock:HomeView')
