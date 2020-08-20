from django import forms
from settings.models import Settings


class ChangeSettings(forms.ModelForm):


    class Meta:
        model = Settings
        fields = (
            'language',
        )
        exclude = (
            'user',
        )
