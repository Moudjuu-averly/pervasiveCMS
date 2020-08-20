from django.urls import re_path
from django.contrib import admin
from . import views
from .views import (
    drive_main_view, #main view
    )

app_name='drive'

urlpatterns = [
    re_path(r'^files/$', views.drive_main_view, name='drive_main_view'), #Main view


    #User tenders
    #re_path(r'^my_tenders/add/$', views.add_tender, name='add_tender'),
    #re_path(r'^tender/update/(?P<slug>[\w-]+)/$', views.update_tender, name='update_tender'),
    #re_path(r'^(?P<slug>[-\w]+)/restore_tender/$', views.restore_tender, name='restore_tender'),
    #re_path(r'^tenders/$', views.corp_all_tender_view, name='corp_all_tender_view'),
    #re_path(r'^tender/(?P<slug>[\w-]+)/$', views.corp_single_tender_view, name='corp_single_tender_view'),
    #re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_tender, name='delete_tender'),
    #re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_tender_permanent, name='delete_tender_permanent'),
    #re_path(r'^search/$', views.search, name='search'),


    ]
