from django import forms
#from django.core.validators import validate_email
from .models import Join, Contact, Subscription, PostMail
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class JoinForm(forms.ModelForm):
    # demail       = forms.EmailInput(
    #                 #widget=forms.EmailInput#
    #
    #                     attrs={
    #                     "type":"email" ,
    #                     "class":"form-control" ,
    #                     "placeholder": "Your email here..."
    #                     })
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'label':'',
            'name':'email',
            'type':'email',
            'id':'id_email',
            #'maxlength':'150',
            #'required':'',
            'class': 'form-control',
            'placeholder': 'Your email here...'
        }
    ))

    class Meta:
        model = Join
        fields = (
        'email',

        )

    def clean_mail(self, *args, **kwargs):
        cleaned_data        = super(Join, self).clean()
        #email = self.cleaned_data.get("email")
        qs                  = Join.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError('You\'re already a member, n\'plz check your spam folder. ')
        return email


class ContactForm(forms.ModelForm):

    full_name           = forms.CharField(widget=forms.TextInput(
        attrs={
            'type':'text',
            'class': 'form-control',
            'placeholder': 'Full name...',
            'data-validation':'required',
        }
    ))
    subject             = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'support_type',
            'id': 'id_subject',
            'data-validation':'required',
        }
    ), choices=Contact.CONTACT_TYPE_CHOICES
    )
    email               = forms.CharField(widget=forms.TextInput(
        attrs={
            'type':'email',
            'class': 'form-control',
            'placeholder': 'Email address...',
            'data-validation':'required',
        }
    ))
    message              = forms.TextInput(
        attrs={
            'type':'textarea',
            'class': 'form-control',
            'placeholder': 'Your message here...',
            'data-validation':'required',
        }
    )


    class Meta:
        model = Contact
        fields = (
            #'to',
            'full_name',
            'subject',
            'email',
            'message',
        )

        exclude = (
            'ip_address',
        )

    def clean_name(self):
        full_name = self.cleaned_data['full_name']
        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        return subject

    def clean_message(self):
        message = self.cleaned_data['message']
        return message
    def clean_contact(self, *args, **kwargs):
        email       = self.cleaned_data.get("email")

        #########------> check Blacklisted emails <-------##########
        ############################################################

        #qs    = Blacklisted.objects.filter(email__iexact=email)
        #if qs.exists():
        #    black_message = 'This email has been blacklisted from contacting this company please' +
        #    'contact ' + to.user.BusinessBaseProfile.help_email to resolve the issue +''
        #    raise forms.ValidationError(black_message)

        #full_name   = self.cleaned_data.get("full_name")
        #message     = self.cleaned_data.get("message")

        #return

class GeneralMailForm(forms.ModelForm):
    tittle = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'heading...',
            'data-validation':'required',
            'data-validation-help':'Provide title.'
        }
    ))
    # mainimage = forms.FileField(widget=forms.FileInput(
    #     attrs={
    #         'class': 'form-control',
    #         'name': 'mainimage',
    #         'type': 'file',
    #         'data-validation':'required',
    #         'data-validation-help':'Upload a mainimage for this please.'
    #     }
    # )
    # )
    post_file = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'post_file',
            'type': 'file',
            'data-validation':'required',
            'data-validation-help':'Upload a post_file for this please.'
        }
    )
    )
    short_description = forms.CharField(
        label='Minimun',
        widget=forms.widgets.TextInput(attrs={
        'type':'textarea',
        'data-validation':'required',
        'class':'form-control input',
        'data-validation-help':'short_description',
        'placeholder': 'short_description'
         }),
    )

    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = PostMail
        fields = (
        'content',
        'tittle',
        # 'mainimage',
        'short_description',
        'post_file',
        )
        exclude = (
        'user',
        'slug',
        )
