from django.urls import re_path
from . import views
from .views import send_mails#, MarketingView

app_name='newsletter'

urlpatterns = [
     #user

     #re_path(r'^marketing/$', MarketingView.as_view(), name='MarketingView'),
     re_path(r'^send-mails/$', views.send_mails, name='send_mails'),
     #re_path(r'^(?P<slug>[\w-]+)/update/$', views.update_job, name='update_job'),
     #re_path(r'^(?P<slug>[-\w]+)/delete/$', views.delete_job, name='delete_job'),
     #re_path(r'^(?P<slug>[-\w]+)/restore_job/$', views.restore_job, name='restore_job'),
     #re_path(r'^(?P<slug>[\w-]+)/view/$', views.corp_single_job_view, name='corp_single_job_view'),
     #url(r'^(?P<slug>[\w-]+)/delete/$', views.delete_job_permanent, name='delete_job_permanent'),




     #re_path(r'^all$', views.view_all_jobs, name='view_all_jobs'), #visitor
     #re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.view_job, name='view_job'),
     #re_path(r'^all/view/$', views.corp_all_job_view, name='corp_all_job_view'), ##visitor
     #re_path(r'^remote-jobs/$', views.remote_jobs, name='remote_jobs'),

     #re_path(r'^filter/<job_type>$', views.filter_job_type, name='filter_job_type'),
     #re_path(r'^search/$', views.search, name='search'),
     ]
