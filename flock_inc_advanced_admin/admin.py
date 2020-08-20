# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Flock Inc master admin'

admin_site = MyAdminSite(name='flock-inc-advanced')
