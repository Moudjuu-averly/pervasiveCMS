from django.urls import re_path
from . import views
from recycle.views import (
    view_all_deleted, deleted_services, deleted_jobs, deleted_products, deleted_tenders
    )

app_name='recycle'

urlpatterns = [
    #user
    re_path(r'^bin/$', views.view_all_deleted, name='view_all_deleted'),
    re_path(r'^services/$', views.deleted_services, name='deleted_services'),
    re_path(r'^jobs/$', views.deleted_jobs, name='deleted_jobs'),
    re_path(r'^products/$', views.deleted_products, name='deleted_products'),
    re_path(r'^tenders/$', views.deleted_tenders, name='deleted_tenders'),
    ]
