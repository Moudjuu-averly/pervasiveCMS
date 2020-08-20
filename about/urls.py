from django.urls import re_path
from . views import plans, testimonies, our_team, faqs, upgrade

app_name='about'

urlpatterns = [
    re_path(r'^plans/$', plans, name='plans'),
    re_path(r'^plans/upgrade/$', upgrade, name='upgrade'),



    re_path(r'^faq\'s/$', faqs, name='faqs'),
    # re_path(r'^request-a-demo/$', faqs, name='request_a_demo'),
]
