from django.urls import re_path
from . import views
from services.views import (
    ServiceView, add_service, view_service, update_service, delete_service,
    view_all_services, filter_service_type, search, corp_single_service_view,
    corp_all_service_view, restore_service
    )

app_name='services'

urlpatterns = [
    #user
    re_path(r'^my_services/$', ServiceView.as_view(), name='ServiceView'),
    re_path(r'^add/$', views.add_service, name='add_service'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', views.update_service, name='update_service'),
    re_path(r'^(?P<slug>[-\w]+)/delete/$', views.delete_service, name='delete_service'),
    re_path(r'^(?P<slug>[-\w]+)/restore_service/$', views.restore_service, name='restore_service'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.corp_single_service_view, name='corp_single_service_view'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_service_permanent, name='delete_service_permanent'),

    #visitor
    re_path(r'^all$', views.view_all_services, name='view_all_services'), #visitor
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.view_service, name='view_service'),
    #re_path(r'^all/view/$', views.corp_all_service_view, name='corp_all_service_view'), ##visitor
    re_path(r'^filter/<service_type>$', views.filter_service_type, name='filter_service_type'),
    re_path(r'^search/$', views.search, name='search'),
    ]
