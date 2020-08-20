from django.urls import re_path, path
from . import views

app_name='support'

urlpatterns = [
    re_path(r'^main/$', views.support_view, name='support_view'),
    re_path(r'^contact/$', views.contact_support, name='contact_support'),

]
