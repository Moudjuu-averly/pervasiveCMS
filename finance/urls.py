#from django.urls import path
#from . import views

from django.urls import re_path
#from path import Path as path
from . views import StarterPackageListView, StarterPackageDetailView

app_name = 'starter'
urlpatterns = [
    re_path('<>', StarterPackageListView.as_view(), name='list'),
    re_path('<slug>', StarterPackageDetailView.as_view(), name='detail'),

]
# urlpatterns = [
#     #url(r'^$', HomeView.as_view(), name='HomeView'),
#     url(r'^packages/$', views.choose_package, name='choose_package'),
# ]
