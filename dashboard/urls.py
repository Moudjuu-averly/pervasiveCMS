from django.urls import re_path
from . import views
from .views import dashboard_view

app_name='dashboard'

urlpatterns = [
    re_path(r'^$', views.dashboard_view, name='dashboard_view'),
    ]
