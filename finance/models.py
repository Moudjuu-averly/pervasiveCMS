# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
#from profiles.models import Profile
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
#import stripe
#stripe.api_key = settings.STRIPE_SECRET_KEY


STARTER = 'S'
REGULAR = 'R'
GOLD = 'G'
PLATINUM = 'P'
MEMBERSHIP_CHOICES = (
    (STARTER, 'starter'),
    (REGULAR, 'Regular'),
    (GOLD, 'Gold'),
    (PLATINUM, 'Platinum'),
    )

class Membership(models.Model):
    slug                    = models.SlugField(default='')
    membership_type         = models.CharField(
            choices=MEMBERSHIP_CHOICES,
            default='',
            max_length=30)
    price                   = models.IntegerField(default=15)
    stripe_plan_id          = models.CharField(max_length=40)

    def __str__(self):
        return self.membership_type

class UserMembership(models.Model):
    user                    = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_membership')
    stripe_customer_id      = models.CharField(max_length=40)
    membership_type         = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s' % (self.user.username, self.membership_type )

def user_membership(sender, **kwargs):
    if kwargs['created']:
        membership = UserMembership.objects.create(user=kwargs['instance'])

post_save.connect(user_membership, sender=User)
#def post_save_usermebership_created(sender, instance, created, *args, **kwargs):
#    if 'created':
#        UserMembership.objects.get_or_create(user=instance)
#    user_membership, created = UserMembership.objects.get_or_create(user=instance)

    #if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
    #    new_customer_id = stripe.Customer.create(email=instance.email)
    #    user_membership.stripe_customer_id = new_customer_id['id']
    #    user_membership.save()
#post_save.connect(post_save_usermebership_created, sender=User)

class SubscriptionManager(models.Manager):

    def calculate_payments(self):
        pass
        #return self.count

        def add(self):
            pass

        def sustract(self):
            pass

        def discount(self):
            pass

class Subscription(models.Model):
    user_membership         = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    stripe_subscription_id  = models.CharField(max_length=40)
    is_active               = models.BooleanField(default=True)

    objects = SubscriptionManager()

    def __str__(self):
        return self.user_membership.user #.username
