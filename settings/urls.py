from django.conf.urls import url, include
from . import views

app_name='settings'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
]
