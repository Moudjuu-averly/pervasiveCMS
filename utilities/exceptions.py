from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError



def image_file_size(self, value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if self.profile_image.size > limit:
        raise ValidationError('File too large. Image Size should not exceed 10 MB.')

def video_file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if self.profile_image.size > limit:
        raise ValidationError('File too large. Video should not exceed 20 MB.')

def video_file_duration(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if self.profile_image.size > limit:
        raise ValidationError('File too large. Video should not exceed 30 Seconds.')
