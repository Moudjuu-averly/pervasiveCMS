from django.urls import re_path
from django.conf import settings
from accounts import views
from . import views

app_name='profiles'

urlpatterns = [
    #re_path(r'^/$', views.view_profile, name='view_profile'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.view_profile_visitor, name='view_profile_visitor'),
    #re_path(r'^pervasive/$', views.edit_pervasive, name='edit_pervasive'),

]
