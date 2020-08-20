from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from django.db import models


class ContactManager(models.Manager):
    def create_request(self,active, full_name, email, subject, message):
        request = self.create(
                            #request_number=request_number,
                            active=active,
                            full_name=full_name,
                            email=email,
                            subject=subject,
                            message=message
                            )
        return request
