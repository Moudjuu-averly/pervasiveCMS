from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


 
def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if self.profile_image.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')
