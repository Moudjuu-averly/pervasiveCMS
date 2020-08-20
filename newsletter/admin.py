# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Join, Contact, Subscribe, PostMail, Subscription
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage
from basecode import settings
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders


# Register your models here.
admin.site.register(Join)
admin.site.register(Contact)
admin.site.register(Subscribe)
admin.site.register(Subscription)
admin.site.register(PostMail)

class PostAdmin(admin.ModelAdmin):
  list_display=('id','title','slug','publish','status','post_file')
  list_filter=('status','created','publish','author')
  readonly_fields=('author','number_of_click')
  search_filter=('title','body')
  prepopulated_fields=({'slug':('title',)})
  raw_id_fields=('author',)
  date_hierarchy='publish'
  ordering=['status','publish']
  #inlines=[ImageAdmin]


  def save_model(self,request,obj,form,change):
        super(PostAdmin,self).save_model(request,obj,form,change)

        if not change and settings.DEBUG==False and obj.status=='published':
            subscribed_visitors = Subscription.objects.all()
            if subscribed_visitors:
                mail_subject = 'Test blog new post: '+ obj.title
                current_site = Profile.objects.get_current()
                domain = 'http://'+current_site.domain+'/'+obj.slug+'/'
                logo = finders.find('favicon.png')
                try:
                    message = get_template('newpost.html').render({'post':obj,'logo':logo,'domain':domain})
                except Exception as e:
                    print(e)

                for visitor in subscribed_visitors:

                    to_email = visitor.email

                    try:
                        send_email = EmailMessage(mail_subject,message,to=[to_email],from_email='info@youremail.com')
                        send_email.content_subtype = 'html'
                        send_email.mixed_subtype = 'related'
                        logo_item = MIMEImage(open(logo,'rb').read(),_subtype='png')
                        logo_item.add_header('Content-ID','<{}>'.format(logo))
                        send_email.attach(logo_item)
                        image = MIMEImage(obj.mainimage.read())
                        image.add_header('Content-ID','<{}>'.format(obj.image_file))
                        send_email.attach(image)
                        send_email.send()
                    except Exception as err:
                        print(err)
