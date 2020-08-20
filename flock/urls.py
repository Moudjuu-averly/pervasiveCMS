from django.urls import re_path
from django.contrib import admin
from . import views

from flock.views import (
    HomeView,
    view_single_flock,
    view_all_flocks,
    post_update,
    post_delete,
    PostLikeToggle,
    PostLikeAPIToggle,
    )

app_name='flock'

urlpatterns = [
    re_path(r'^$', HomeView.as_view(), name='HomeView'),
    re_path(r'^<slug>/$', views.view_single_flock, name='view_single_flock'),
    re_path(r'^search/$', views.search, name='search'),
    re_path(r'^all/$', views.view_all_flocks, name='view_all_flocks'),
    re_path(r'^(?P<slug>[\w-]+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
    re_path(r'^api/(?P<slug>[\w-]+)/like/$', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
    re_path(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends'),
]
