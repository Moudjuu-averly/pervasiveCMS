from django.urls import re_path
import django_sb_admin.views

app_name='django_sb_admin'

urlpatterns = [
    re_path(r'^$', django_sb_admin.views.start, name='sb_admin_start'),
    re_path(r'^dashboard/$', django_sb_admin.views.dashboard, name='sb_admin_dashboard'),
    re_path(r'^charts/$', django_sb_admin.views.charts, name='sb_admin_charts'),
    re_path(r'^tables/$', django_sb_admin.views.tables, name='sb_admin_tables'),
    re_path(r'^forms/$', django_sb_admin.views.forms, name='sb_admin_forms'),
    re_path(r'^bootstrap-elements/$', django_sb_admin.views.bootstrap_elements, name='sb_admin_bootstrap_elements'),
    re_path(r'^bootstrap-grid/$', django_sb_admin.views.bootstrap_grid, name='sb_admin_bootstrap_grid'),
    re_path(r'^rtl-dashboard/$', django_sb_admin.views.rtl_dashboard, name='sb_admin_rtl_dashboard'),
    re_path(r'^blank/$', django_sb_admin.views.blank, name='sb_admin_blank'),
]
