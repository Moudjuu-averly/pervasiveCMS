from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from accounts.models import SocialProfiles
from profiles.models import Profile
from django.core.validators import *

class RegistrationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    username                = forms.CharField(required=True, widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group form-group-no-border',
             'placeholder': 'Username...'
         }
     ))
    email                   = forms.EmailField(required=True, widget=forms.TextInput(
         attrs={
             'class': 'form-control input-group form-group-no-border',
             'placeholder': 'email...'
         }
     ))
    password1               = forms.CharField(required=True, label='Password', widget=forms.PasswordInput(
         attrs={
             'class': 'form-control input-group form-group-no-border',
             'placeholder': 'Password...'
         }
     ))
    password2               = forms.CharField(required=True, label='Password confirmation', widget=forms.PasswordInput(
         attrs={
             'class': 'form-control input-group form-group-no-border',
             'placeholder': 'Password confirm...'
         }
     ))

    class Meta:
        model               = User
        fields              = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def validate_company_name_exist(self):
        cleaned_data        = super(RegistrationForm, self).clean()
        username            = self.cleaned_data.get('username')
        email               = self.cleaned_data.get('email')
        try:
            if username and User.objects.filter(username__iexact=username).exists():
                if email and User.objects.filter(email__iexact=email).exists():
                    raise forms.ValidationError('email', 'A Business with that email already exists.')
                raise forms.ValidationError('company_name', 'A Business with that name already exists.')
        except:
            User.DoesNotExist
        return username, email

    def clean_password2(self):
        # Check that the two password entries match
        password1           = self.cleaned_data.get("password1")
        password2           = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password1

    def save(self, commit=True):
        user                = super(RegistrationForm, self).save(commit=False)
        user.username       = self.cleaned_data["username"]
        user.email          = self.cleaned_data["email"]
        user.set_password   = self.cleaned_data["password1"]
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    template_name           ='/something/else'

    #password                = ReadOnlyPasswordHashField()

    class Meta:
        model               = User
        fields              = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password'
        )

class EditPervasive(forms.ModelForm):

    class Meta:
        model               = Profile
        widgets = {'country': CountrySelectWidget()}
        fields              = (
            '__all__'
        )
        exclude             = (
            'user',
            'slug',
            'likes',
            'country',
        )

    # def url_valid_clean(self):
    #     url                 = super(EditPervasive, self).clean()
    #     url_validator       = URLValidator()
    #     try:
    #         url_validator(url)
    #     except:
    #         raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. https://www.google.com')
    #     return url

class SocialProfilesForm(forms.ModelForm):
    template_name           ='/something/else'

    class Meta:
        model               = SocialProfiles
        fields              = (
            '__all__'
        )
        exclude             = (
            'user',
        )

    def url_valid_clean(self):
        url                 = super(SocialProfilesForm, self).clean()
        url_validator       = URLValidator()
        try:
            url_validator(url)
        except:
            raise forms.ValidationError(code='invalid url', value='Please type a valid link address e.g. http://www.google.com')
        return url
