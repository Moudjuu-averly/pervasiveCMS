from django.urls import re_path
from . views import pervasive_view, product_n_services, validate_email
from profiles.views import single_post

app_name='pervasive'


urlpatterns = [
    re_path(r'^$', pervasive_view, name='pervasive_view'),
    re_path(r'^validate_email/$', validate_email, name='validate_email'),
    re_path(r'^blog/(?P<slug>[\w-]+)/$', single_post, name='single_post'), 
    re_path(r'^product-n-services/$', product_n_services, name='product_n_services'),
    # re_path(r'^pervasive/$', trending, name='trending_view'),
    # re_path(r'^pervasive/$', jobs, name='jobs_view'),
    # re_path(r'^pervasive/$', tender, name='tender_view'),
    # re_path(r'^pervasive/$', scholarship, name='trending_view'),
    # re_path(r'^pervasive/$', blogs, name='blogs_view'),


]
