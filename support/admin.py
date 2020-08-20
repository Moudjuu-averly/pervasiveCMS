# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Support

class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        Model = Support
        fields = ('__all__')
        #read_only_fields =( 'viewed_by_ip', 'seen_by_us')

admin.site.register(Support)
