from django.urls import re_path
from django.contrib import admin
from . import views
from .views import SearchView, search

app_name='search'

urlpatterns = [
    re_path(r'^$', SearchView.as_view(), name='search_view'),
    re_path(r'^', views.search, name='search'),
]
 
