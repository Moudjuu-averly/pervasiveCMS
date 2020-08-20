from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from accounts.models import SocialProfiles
from profiles.models import Profile
from django.core import validators
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from utilities.exceptions import image_file_size, video_file_size, video_file_duration
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class EditDisplay(forms.ModelForm):
    template_name           ='/something/else'

    official_business_name = forms.CharField(required=True, label='Company full name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'official_business_name',
            'data-validation':'required',
            'placeholder': 'E.g Creative Code Inc'
        }
    )
    )

    business_type               = forms.ChoiceField(widget=forms.Select(
         attrs={
             'class': 'form-control',
             'name': 'business_type',
             'selected': 'selected',
             'data-validation':'required',
         }
     ), choices=Profile.BUS_TYPE_CHOICES
     )

    country_origin = CountryField().formfield()
    country_origin.input_type = 'select'
    country_origin.template_name = 'django/forms/widgets/select.html'
    country_origin.option_template_name = 'django/forms/widgets/select_option.html'

    country_city               = forms.CharField(required=True, label='Country of Origin', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'name': 'country_city',
             'placeholder': 'e.g Los angels',
             'data-validation':'required'
         }
     ))
    address               = forms.CharField(required=True, label='Address', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'name':'address',
             'data-validation':'required',
             'placeholder': '69 Indipendance Avenue'
         }
     ))
     #About (A short description About the company)
    about               = forms.CharField(required=True, label='About', widget=forms.Textarea(
         attrs={
             'class': 'form-control input-group',
             'name':'about',
             'data-validation':'required',
             'placeholder': 'Lamborghini Mercy, Your chick she so thirsty, I\'m in that two seat Lambo.'
         }
     ))
    widgets = {'country_origin': CountrySelectWidget()}
    about = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model               = Profile

        fields              = (
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
        )
        exclude             = (
        #'__all__'
            'user',
            'slug',
            'likes',
        )


class EditContact(forms.ModelForm):
    template_name           ='/something/else'

    support_email               = forms.EmailField(validators=[URLValidator], required=True, label='Support email', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'e.g support@deamate.com',
             'name': 'support_email',
             'type': 'email',
             'data-validation':'required',
         }
     ))
    email_address               = forms.EmailField(validators=[URLValidator], required=True, label='Info email address', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'e.g info@deamate.com',
             'name': 'email_address',
              'type': 'email',
             'data-validation':'required',
         }
     ))
    office_phone               = forms.IntegerField(validators=[URLValidator], required=True, label='Office number', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': '+0000 000 000',
             'name': 'office_phone',
             'type': 'number',
             'data-validation':'required',
         }
     ))
    contact_cell               = forms.IntegerField(validators=[URLValidator], required=True, label='Contact cell', widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': '+0000 000 000',
             'name': 'contact_cell',
             'type': 'number',
             'data-validation':'required',
         }
     ))
    website               = forms.CharField(validators=[URLValidator], required=True, label='Website', widget=forms.URLInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'www.google.com',
             'name': 'website',
             'data-validation':'required',

         }
     ))
    blog               = forms.CharField(validators=[URLValidator], required=True, label='Blog', widget=forms.URLInput(
         attrs={
             'class': 'form-control input-group',
             'placeholder': 'www.blogs.mediumpoint.com/deamte',
             'name': 'blog',
             'data-validation':'required',
         }
     ))

    class Meta:
        model               = Profile
        widgets = {'country': CountrySelectWidget()}
        fields              = (
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'website',
            'blog',
        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
        )

        # def validate_url_in_use_by_someonelse(self):
        #     cleaned_data        = super(RegistrationForm, self).clean()
        #     username            = self.cleaned_data.get('username')
        #     email               = self.cleaned_data.get('email')
        #     try:
        #         if username and User.objects.filter(username__iexact=username).exists():
        #             if email and User.objects.filter(email__iexact=email).exists():
        #                 raise forms.ValidationError('email', 'A Business with that email already exists.')
        #             raise forms.ValidationError('company_name', 'A Business with that name already exists.')
        #     except:
        #         User.DoesNotExist
        #     return username, email

class EditMedia(forms.ModelForm):
    template_name           ='/something/else'


    profile_image               = forms.CharField(required=True, label='Profile Picture', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    cover_image                = forms.CharField(required=True, label='Cover Image', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    about_video                = forms.CharField(required=True, label='About video', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    who_we_are_video                = forms.CharField(required=True, label='Who we are', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    services_video                = forms.CharField(required=True, label='Services', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    projects_video                = forms.CharField(required=True, label='Projects', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'profile_image',
            'cover_image',
            'about_video',
            'who_we_are_video',
            'services_video',
            'projects_video',
        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
        )

class ProfileImageForm(forms.ModelForm):
    template_name           ='profiles/edit/media/profile_image.html'


    profile_image = forms.FileField(widget=forms.FileInput(
         attrs={
             'class': 'form-control',
             'name': 'profile_image',
             'type': 'file',
             'data-validation':'required',
         }
     ))
    projects_video = forms.FileField(widget=forms.FileInput(
         attrs={
             'class': 'form-control',
             'name': 'profile_image',
             'type': 'file',
             'data-validation':'required',
         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'profile_image',
            'projects_video',

        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
            'cover_image',
            'about_video',
            'who_we_are_video',
            'services_video',
            #'projects_video',
        )

class ProfileCoverImageForm(forms.ModelForm):
    template_name           ='profiles/edit/media/cover_image.html'


    cover_image               = forms.FileField(required=True, validators=[image_file_size], label='Profile Image', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
             'accept': 'image/*',
             'type': 'file',

         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'cover_image',

        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
            'profile_image',
            'about_video',
            'who_we_are_video',
            'services_video',
            'projects_video',
        )

class ProfileAboutVideoForm(forms.ModelForm):
    template_name           ='profiles/edit/media/about_video.html'


    about_video               = forms.CharField(required=True, validators=[video_file_size], label='About Video', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
             'accept': 'video/*',
             'type': 'file',
         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'about_video',

        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
            'cover_image',
            'profile_image',
            'who_we_are_video',
            'services_video',
            'projects_video',
        )

class ProfileWhoWeAreVideoForm(forms.ModelForm):
    template_name           ='profiles/edit/media/who_we_are_video.html'


    who_we_are_video               = forms.CharField(required=True, validators=[video_file_size], label='Who We Are Video', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
             'accept': 'video/*',
             'type': 'file',
         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'who_we_are_video',

        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
            'cover_image',
            'about_video',
            'profile_image',
            'services_video',
            'projects_video',
        )

class ProfileServicesVideoForm(forms.ModelForm):
    template_name           ='profiles/edit/media/services_video.html'


    services_video               = forms.CharField(required=True, validators=[video_file_size], label='Service Video', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
             'accept': 'services/*',
             'type': 'file',
         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'services_video',

        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
            'cover_image',
            'profile_image',
            'who_we_are_video',
            'about_video',
            'projects_video',
        )

class ProfileProjectsVideoForm(forms.ModelForm):
    template_name           ='profiles/edit/media/projects_video.html'


    projects_video               = forms.CharField(required=True, validators=[image_file_size], label='Projects Video', widget=forms.FileInput(
         attrs={
             'class': 'form-control input-group',
         }
     ))
    class Meta:
        model               = Profile
        fields              = (
            'projects_video',

        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'official_business_name',
            'business_type',
            'country_origin',
            'country_city',
            'address',
            'about',
            'support_email',
            'email_address',
            'office_phone',
            'contact_cell',
            'Website',
            'blog',
            'cover_image',
            'about_video',
            'profile_image',
            'services_video',
            'who_we_are_video',
        )
