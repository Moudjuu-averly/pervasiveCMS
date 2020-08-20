# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.http  import * #is_ajax
from . forms import ContactForm, GeneralMailForm
from . models import Contact
from .models import Join, Contact, Subscribe, PostMail, Subscription
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, EmailMessage
from basecode import settings
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders


class HomePageListView(FormView):
    form_class= ContactForm
    template_name='home.html'
    def get(self,request):
         form = ContactForm()
         return super(HomePageListView, self).get(request, form=form)

    def post(self, request, *args, **kwargs):
          if request.is_ajax():
              error = None
              success = None
              try:
                  active = True
                  #is_paid_member = False
                  email = request.POST['email']

                  #if ContactForm.objects.filter(email=email).exists():
                    #  user = User.objects.get(email=email)
                  #else:
                    #  user = None
                  #if user:
                    #  is_registered = True
                     # if user.user_type != 'Basic':is_paid_member = True
                  #request_number = get_random_string(8)
                  new_request = ContactData.objects.create_request(
                                      #request_number,is_registered,is_paid_member,
                                      request.POST['name'],email,request.POST['subject'],request.POST['message'])
                  new_request.save()
                  success = 'Ok'
              except Exception as e:
                  error = CONTACT_FORM_ERROR

              if error :
                  return HttpResponse(error)
              else:
                  return HttpResponse(success)


from django.conf import settings
from django.core.mail import send_mail
subject = 'Thank you for registering to our site'
message = ' it  means a world to us '
email_from = settings.EMAIL_HOST_USER
recipient_list = ['lebeusmm@gmail.com', 'lebeusm@yahoo.com']
#send_mail( subject, message, email_from, recipient_list )



# @login_required
def send_mails(request, instance):
      #super(PostAdmin,self).save_model(request,obj,form,change)

      #if not change and settings.DEBUG==False and obj.status=='published':
      subscribed_visitors = Subscription.objects.all()
      if subscribed_visitors:
          mail_subject = 'Test blog new post: '+ instance.tittle
          content = instance.content
          current_site = Profile.objects.get_current()
          domain = 'http://'+current_site.domain+'/'+instance.slug+'/'
          logo = finders.find('favicon.png')
          try:
              message = get_template('profiles/mails/general/normal_mail_post.html').render({'content':content,'logo':logo,'domain':domain})
          except Exception as e:
              print(e)

          for visitor in subscribed_visitors:

              to_email = visitor.email

              try:
                  send_email = EmailMessage(mail_subject,message,to=[to_email],from_email='noreply@support.basecode.com')
                  send_email.content_subtype = 'html'
                  send_email.mixed_subtype = 'related'
                  logo_item = MIMEImage(open(logo,'rb').read(),_subtype='png')
                  logo_item.add_header('Content-ID','<{}>'.format(logo))
                  send_email.attach(logo_item)
                  image = MIMEImage(instance.mainimage.read())
                  image.add_header('Content-ID','<{}>'.format(instance.image_file))
                  send_email.attach(image)
                  send_email.send()
              except Exception as err:
                  print(err)

# @login_required
def send_mails(request):
    template_name = 'profiles/marketing/mails/general/send_mail.html'
    form = GeneralMailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        #instance.save()

        subscribed_visitors = Subscription.objects.filter(is_active=True).all()
        if subscribed_visitors:
            mail_subject = 'Test blog new post: '+ instance.tittle
            message = ''
            content = instance.content
            #current_site =  request.get_host()
            domain = 'http://'+ 'www.basecode.com/blog' +'/'+instance.slug+'/'
            #logo = finders.find('favicon.png')
            #try:
                #message = get_template('profiles/mails/general/normal_mail_post.html').render({'content':content, 'domain':domain})
            #except Exception as e:
            #    print(e)

            for visitor in subscribed_visitors:

                to_email = visitor.email
                message=instance.content
                try:
                    send_email = EmailMessage(mail_subject,message,from_email=settings.EMAIL_HOST_USER,to=[to_email])
                    send_email.content_subtype = 'html'
                    send_email.mixed_subtype = 'related'
                    #logo_item = MIMEImage(open(logo,'rb').read(),_subtype='png')
                    #logo_item.add_header('Content-ID','<{}>'.format(logo))
                    #send_email.attach(logo_item)
                    #image = MIMEImage(instance.post_file.read())
                    #image.add_header('Content-ID','<{}>'.format(instance.post_file))
                    #send_email.attach(image)
                    send_email.send()
                except Exception as err:
                    print(err)


        instance.save()



        return redirect('jobs:JobView')
        print(form.errors)
    else:
        form = GeneralMailForm(request.POST or None, request.FILES or None)

    context = {
        'form': form,
        "title": 'Jobs | add',
    }
    return render(request, template_name, context)
