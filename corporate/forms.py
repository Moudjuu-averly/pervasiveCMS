from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#from django_countries.widgets import CountrySelectWidget
#from django_countries.fields import CountryField
from corporate.models import CompanyProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            #'first_name',
            #'last_name',
            'email',
            'password1',
            'password2'
        )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        #user.first_name = self.cleaned_data['first_name']
        #user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            #'first_name',
            #'last_name',
            'password',
        )


class EditCompany(forms.ModelForm):
    template_name='/something/else'
    #country = CountryField().formfield()

    class Meta:
        model = CompanyProfile
        #widgets = {'country': CountrySelectWidget()}
        fields = (
            '__all__'
        )
        exclude = (
            'user',
            #'country',
        )
