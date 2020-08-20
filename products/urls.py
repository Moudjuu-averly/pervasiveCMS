from django.urls import re_path
from . import views
from products.views import (
    ProductView, add_product, view_product, update_product, delete_product,
    view_all_products, filter_product_type, search, corp_single_product_view,
    corp_all_product_view, restore_product
    )

app_name='products'

urlpatterns = [
    #user
    re_path(r'^my_products/$', ProductView.as_view(), name='ProductView'),
    re_path(r'^add/$', views.add_product, name='add_product'),
    re_path(r'^(?P<slug>[\w-]+)/update/$', views.update_product, name='update_product'),
    re_path(r'^(?P<slug>[-\w]+)/delete/$', views.delete_product, name='delete_product'),
    re_path(r'^(?P<slug>[-\w]+)/restore_product/$', views.restore_product, name='restore_product'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.corp_single_product_view, name='corp_single_product_view'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', views.delete_product_permanent, name='delete_product_permanent'),




    re_path(r'^all$', views.view_all_products, name='view_all_products'), #visitor
    re_path(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.view_product, name='view_product'),
    re_path(r'^filter/<product_type>$', views.filter_product_type, name='filter_product_type'),
    re_path(r'^search/$', views.search, name='search'),
    ]
