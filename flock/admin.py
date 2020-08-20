# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from flock.models import Post, Friend, Comments

class PostModelAdmin(admin.ModelAdmin):
#     list_display = ["user", "post_image","title", "updated", "timestamp"]
#     list_display_links = ["updated"]
#     list_editable = ["title"]
#     list_filter = ["updated", "timestamp"]
#
     search_fields = ["title", "user"]
     class Meta:
         model = Post
#
#
# admin.site.register(Post, PostModelAdmin)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Friend)
