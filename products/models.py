# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import *
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg, Max, Min, Q, Count, FloatField
from .manager import ProductManager
from ckeditor_uploader.fields import  RichTextUploadingField
from autoslug import AutoSlugField
from .utils import *


class Product(models.Model):
    #product type choices
    HEALTH_BEAUTY_COSMETICS         = '1'
    FOOD_N_BEVERAGES                = '2'
    BAGS_SHOES_ACCESSORIES          = '3'
    AUTO_TRANSPORTATION             = '4'
    EDUCATION_TRAINING              = '5'
    APPAREL_TEXTILES_ACCESSORIES    = '6'
    ELECTRONICS                     = '7'
    AIRLINE_SHUTTLE                 = '8'
    AGRICULTURE                     = '9'
    VISA                            = '10'
    TOURISIM_HOSPITALITY            = '11'
    HOME_LIGHT_CONSTRUCTION         = '12'
    GIFTS_SPORTS_TOYS               = '13'
    ELECTRICAL_COMPONENTS_TELECOMS  = '14'
    OTHER                           = '15'

    PRODUCT_CATEGORY_CHOICES = (
        (HEALTH_BEAUTY_COSMETICS, 'Health, beatuy and Cosmetics'),
        (FOOD_N_BEVERAGES, 'Food and Beverages'),
        (BAGS_SHOES_ACCESSORIES, 'Bags, Shoes and Accessories'),
        (AUTO_TRANSPORTATION, 'Auto and  Transportation'),
        (EDUCATION_TRAINING, 'Education and Training'),
        (APPAREL_TEXTILES_ACCESSORIES, 'Apparel, textiles and Accessories'),
        (AIRLINE_SHUTTLE, 'Airline and Shuttle'),
        (ELECTRONICS, 'Electronics'),
        (ELECTRICAL_COMPONENTS_TELECOMS, 'Electrical Equipment, Components and Telecoms'),
        (AGRICULTURE, 'Agriculture and Food'),
        (VISA, 'Visa'),
        (TOURISIM_HOSPITALITY, 'Tourism and Hospitality'),
        (HOME_LIGHT_CONSTRUCTION, 'Home, Lights and Construction'),
        (GIFTS_SPORTS_TOYS, 'Gifts, Sports and Toys'),
        (OTHER, 'Other'),
    )

    NORMAL      = '1'
    SPECIAL     = '2'
    PROMO       = '3'
    SALETYPE = (
        (NORMAL, 'Normal'),
        (SPECIAL, 'Special'),
        (PROMO, 'Promo'),

    )
    #short details
    user                        = models.ForeignKey(User, on_delete=models.CASCADE)
    product_tittle              = models.CharField(max_length=255, null=False)
    slug                        = AutoSlugField(unique=True, editable=True, populate_from='product_tittle',
                        unique_with=['user', 'created'])
    content               = RichTextUploadingField()
    product_type                = models.CharField(
                                max_length=50,
                                choices=PRODUCT_CATEGORY_CHOICES,
                                default=FOOD_N_BEVERAGES,
            )
    sale_type                    = models.CharField(
                                max_length=50,
                                choices=SALETYPE,
                                default=NORMAL,
            )
    product_video               = models.FileField(upload_to='videos/products/product_video', null=True, blank=True)
    rating                      = models.FloatField(blank=False, null=True)#suppose is a ForeignKey field
    views                       = models.IntegerField(blank=True, null=True, default=0)#
    view_by                     = models.GenericIPAddressField(default='127.0.0.1')
    deleted                     = models.BooleanField(default=False)
    edited                      = models.BooleanField(default=False)

    #salary
    start_price                 = models.FloatField(blank=False, null=False, default=150.00)
    end_price                   = models.FloatField(blank=False, null=True)

    #time and date
    created                     = models.DateTimeField(auto_now_add=True)
    last_edited                 = models.DateTimeField(auto_now=True)
    last_accessed               = models.DateTimeField(auto_now=True)
    active                      = models.BooleanField(default=True)

    #call the manager
    objects                     = ProductManager()

    class Meta:
        ordering         = ('-created', '-last_edited' )

    def __str__(self):
        return '%s %s' % (self.product_tittle, self.user)

    def __unicode__(self):
        return str(self.product_video)

def post_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

post_save.connect(post_save_receiver, sender=Product)
