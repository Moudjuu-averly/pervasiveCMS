from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from django.core.validators import URLValidator
from . models import Tender,  TenderApplicant, Scholarship, Announce
from ckeditor_uploader.widgets import  CKEditorUploadingWidget


class TenderForm(forms.ModelForm):
    template_name           ='/something/else'


    tender_tittle                = forms.CharField(required=True, widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'E.g Upgrade of mtc Data centers',
             'name': 'tender_tittle',
             'type': 'text',
             'data-validation':'required',
             'data-validation-help':'Provide a tender tittle.'
         }
     ))
    city               = forms.CharField(required=True, label='Info email address', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'e.g Cape town',
             'name': 'city',
             'type': 'text',
             'data-validation':'required',
             'data-validation-help':'Your location.'
         }
     ))
    contact_person_name               = forms.CharField(required=True, label='Office number', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'Will Smith',
             'name': 'contact_person_name',
             'type': 'text',
             'data-validation':'required',
             'data-validation-help':'Contact details for enquiries.'
         }
     ))
    office_no            = forms.IntegerField(required=True, label='Office Number', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': '+0000 000 000',
             'type': 'number',
             'data-validation':'required',
             'data-validation-help':'Provide a valid number please.'
         }
     ))
    address            = forms.CharField(required=True, label='Business type', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-group',
            'placeholder': 'e.g 123 Business street, Abuja',
            'name': 'address',
            'type': 'text',
            'data-validation':'required',
            'data-validation-help':'Provide a valid address please.'
        }
    ))
    tender_video = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'tender_video',
            'type': 'file',
            'data-validation':'required',
            'data-validation-help':'Upload a video for this tender please.'
        }
    )
    )
    due_date = forms.DateField(
        label='Due Date',
        widget=forms.widgets.DateInput(attrs={
        'type':'date',
        'name':'due_date',
        'id':'datetimepicker',
        'class':'form-control date-picker',
        'data-datepicker-color':'primary',
        'data-validation':'required',
        'data-validation-help':'Please provide a valid future date.'
         }),
    )
    levy_price = forms.CharField(
        label='Minimun',
        widget=forms.widgets.TextInput(attrs={
        'name':'levy_price',
        'type':'number',
        'data-validation':'required',
        'class':'form-control input',
        'data-validation-help':'Provide an amount greater than N$ 100.00.',
        'placeholder': '$200.00'
         }),
    )
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model               = Tender
        fields              = (
            '__all__'
        )
        exclude             = (
            'user',
            'slug',
            'views',
            'view_by',
            'advtised_before',
            'created',
            'edited',
            'active',
        )


    def url_valid_clean(self):
        url                 = super(TenderForm, self).clean()
        url_validator       = URLValidator()
        try:
            url_validator(url)
        except:
            raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. http://www.google.com')
        return url


class EditTenderForm(forms.ModelForm):
    template_name           ='/something/else'


    tender_tittle                = forms.CharField(required=True, widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'E.g Upgrade of mtc Data centers'
         }
     ))
    city               = forms.CharField(required=True, label='Info email address', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'e.g Cape town'
         }
     ))
    contact_person_name               = forms.CharField(required=True, label='Contact person', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'Will Smith',
             'name': 'contact_person_name'
         }
     ))
    office_no            = forms.IntegerField(required=True, label='Office Number', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': '+0000 000 000'
         }
     ))
    address            = forms.CharField(required=True, label='Business type', widget=forms.TextInput(
        attrs={
            'class': 'form-control input-group',
            'placeholder': 'e.g 123 Business street, Abuja'
        }
    ))
    tender_video = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'tender_video',
            'type': 'file',
            'data-validation':'required',
            'data-validation-help':'Upload a video for this tender please.'
        }
    )
    )
    content = forms.CharField(widget=CKEditorUploadingWidget())


    class Meta:
        model               = Tender
        fields              = (
            'address',
            'city',
            'tender_video',
            'content',
            'tender_tittle',
            'contact_person_name',
            'office_no',

        )
        exclude             = (
            'user',
            'views',
            'view_by',
            'due_date',
            'created',
            'edited',
            'active',
        )


    def url_valid_clean(self):
        url                 = super(TenderForm, self).clean()
        url_validator       = URLValidator()
        try:
            url_validator(url)
        except:
            raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. http://www.google.com')
        return url


class TenderApplicantForm(forms.ModelForm):
    template_name           ='/something/else'

    class Meta:
        model               = TenderApplicant
        fields              = (
            '__all__'
        )
        exclude             = (
            'user',
            'due_date',
            'created',
            'active',

        )

    def url_valid_clean(self):
        url                 = super(SocialProfilesForm, self).clean()
        url_validator       = URLValidator()
        try:
            url_validator(url)
        except:
            raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. http://www.google.com')
        return url


class ScholarshipForm(forms.ModelForm):
    template_name           ='/something/else'

    class Meta:
        model               = Scholarship
        fields              = (
            '__all__'
        )
        exclude             = (
            'user',
            'due_date',
            'created',
            'active',
        )

    def url_valid_clean(self):
        url                 = super(SocialProfilesForm, self).clean()
        url_validator       = URLValidator()
        try:
            url_validator(url)
        except:
            raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. http://www.google.com')
        return url


class AnnounceForm(forms.ModelForm):
    template_name           ='/something/else'

    announce_tittle               = forms.CharField(required=True, label='Announcement title', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'e.g 28 09 19 show'
         }
     ))
    announce_type = forms.ChoiceField(widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'announce_type',
            'data-validation':'required',
        }
    ), choices=Announce.ANNOUNCE_TYPE_CHOICES
    )

    announce_image = forms.FileField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'name': 'announce_image',
            'type': 'file',
        }
    )
    )
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model               = Announce
        fields              = (
            'announce_tittle',
            'content',
            'announce_type',
            'announce_image',
        )
        exclude             = (
            'user',
            'slug',
            'deleted',
            'edited',
            'views',
            'rating',
            'last_edited',
            'last_accessed',
            'rating',
            'due_date',
            'created',
            'active',
        )

    def url_valid_clean(self):
        url                 = super(SocialProfilesForm, self).clean()
        url_validator       = URLValidator()
        try:
            url_validator(url)
        except:
            raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. http://www.google.com')
        return url
