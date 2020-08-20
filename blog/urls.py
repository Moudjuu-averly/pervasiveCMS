from django.urls import re_path
from . import views
from blog.views import (
    single_blog,
    view_all_blogs,
    )

app_name='blog'

urlpatterns = [
    re_path(r'^view/(?P<slug>[\w-]+)/$', views.single_blog, name='single_blog'),
    re_path(r'^all/$', views.view_all_blogs, name='view_all_blogs'),
    # re_path(r'^view/(?P<slug>[\w-]+)/news/$', views.single_news, name='single_news'),
    re_path(r'^news/$', views.view_all_news, name='view_all_news'),
    ]
