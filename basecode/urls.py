"""basecode URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path, include, path
from django.contrib import admin
from basecode import views, settings
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from accounts.admin import admin_site
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^$', views.login_redirect, name='login_redirect'),
    re_path(r'^account/$', views.login_redirect, name='login_redirect'),
    #path(r'^vimage-admin/', admin.site.urls),#sys dba
    re_path(r'^pervasive-admin/', include('django_sb_admin.urls')),
    #re_path('flock-inc-admin/', admin_site.urls),#management-decision
    #re_path('flock-master-admin/', admin_site.urls),#top level-strategy
    #re_path(r'^account/', include('accounts.urls'),
    re_path(r'^account/', include('accounts.urls', namespace='accounts')),
    re_path(r'^', include('pervasive.urls', namespace='pervasive')),
    re_path(r'^finance/', include('finance.urls', namespace='finance')),
    re_path(r'^flock/', include('flock.urls', namespace='flock')),
    re_path(r'^', include('profiles.urls', namespace='profiles')),
    re_path(r'^blog/', include('blog.urls', namespace='blog')),
    re_path(r'^jobs/', include('jobs.urls', namespace='jobs')),
    re_path(r'^admanager/', include('adclass.urls', namespace='adclass')),
    re_path(r'^products/', include('products.urls', namespace='products')),
    re_path(r'^services/', include('services.urls', namespace='services')),
    re_path(r'^newsletter/', include('newsletter.urls', namespace='newsletter')),
    re_path(r'^recycle/', include('recycle.urls', namespace='recycle')),
    re_path(r'^support/', include('support.urls', namespace='support')),
    re_path(r'^drive/', include('drive.urls', namespace='drive')),
    re_path(r'^search/', include('search.urls', namespace='search')),
    #re_path(r'^dashboard/', include('dashboard.urls', namespace='dashboard')),


    #re_path(r'^utilities/', include('utilities.urls')),
    re_path(r'^about/', include('about.urls', namespace='about')),
    #re_path(r'^pay-pal/', include('pay-pal.urls')),
    #re_path(r'^administration/', include('administration.urls')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + staticfiles_urlpatterns()

# if settings.DEBUG404:
#     urlpatterns += urlpatterns('',
#         (r'^static/(?P<path>.*)$', staticserve,
#             {'document_root': os.path.join(os.path.dirname(__file__), 'static')} ),
#         )

handler404 = views.handler404
handler500 = views.handler500

#handler403 = 'mysite.views.my_custom_permission_denied_view'
#handler403 = 'mysite.views.my_custom_permission_denied_view'

#The bad_request() view is overridden by handler400:
#handler400 = 'mysite.views.my_custom_bad_request_view'
