from django.urls import re_path
from django.contrib import admin
from . import views
from adclass.views import (
    AdClassView, #main view
    add_tender, add_announce, # add views
    view_tender,
    update_tender,
    delete_tender,
    delete_tender_permanent,
    view_all_tenders,
    filter_tender_type,
    search,
    corp_single_tender_view, corp_single_announce_view, # single objects views
    corp_all_tender_view, corp_all_announce_view, #all objects views
    #FreelancerView,
    #TenderView,

    )

app_name='adclass'

urlpatterns = [
    re_path(r'^all/$', AdClassView.as_view(), name='AdClassView'), #Main view


    #User tenders
    re_path(r'^my_tenders/add/$', views.add_tender, name='add_tender'),
    re_path(r'^tender/update/(?P<slug>[\w-]+)/$', views.update_tender, name='update_tender'),
    re_path(r'^(?P<slug>[-\w]+)/restore_tender/$', views.restore_tender, name='restore_tender'),
    re_path(r'^tenders/$', views.corp_all_tender_view, name='corp_all_tender_view'),
    re_path(r'^tender/(?P<slug>[\w-]+)/$', views.corp_single_tender_view, name='corp_single_tender_view'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_tender, name='delete_tender'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_tender_permanent, name='delete_tender_permanent'),
    re_path(r'^search/$', views.search, name='search'),

    #announcements
    re_path(r'^announce/add/$', views.add_announce, name='add_announce'),
    #re_path(r'^announce/update/(?P<slug>[\w-]+)/$', views.update_tender, name='update_tender'),
    #re_path(r'^(?P<slug>[-\w]+)/restore_tender/$', views.restore_tender, name='restore_tender'),
    re_path(r'^announce/$', views.corp_all_announce_view, name='corp_all_announce_view'),
    re_path(r'^announce/(?P<slug>[\w-]+)/$', views.corp_single_announce_view, name='corp_single_announce_view'),
    #re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_tender, name='delete_tender'),
    #re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_tender_permanent, name='delete_tender_permanent'),
    #re_path(r'^search/$', views.search, name='search'),


    #Visitor
    re_path(r'^tender/(?P<slug>[\w-]+)/$', views.view_tender, name='view_tender'),
    re_path(r'^all/$', views.view_all_tenders, name='view_all_tenders'), #visitor
    re_path(r'^filter/<job_type>$', views.filter_tender_type, name='filter_tender_type'),
    ]
