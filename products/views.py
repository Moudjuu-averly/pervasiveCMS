# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import RedirectView
from django.utils import timezone
from django.views.generic import TemplateView, ListView, DetailView
from itertools import chain
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import ProductForm, UpdateProductForm
from products.models import Product
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def get_ip(request):
    try:
        x_foward = request.META.get("HTTP_X_FOWARDED_FOR")
        if x_foward:
            ip = x_foward.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = ''
    return ip

#Visitor
def view_all_products(request):
    products               = Postproduct.objects.filter(active=True).filter(deleted=False).all()
    paginator = Paginator(products, 15) # Show 25 products per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
    }
    return render(request, 'pervasive/adclass/products/all_products.html', context )

#Visitor
def view_product(request, pk, slug):
    product = list()
    try:
        product               = get_object_or_404(Postproduct, pk=pk, slug=slug)

        '''' Record the last accessed date and number of view'''
        product.last_accessed = timezone.now()
        '''model manager function with ip address META option'''
        view_by           = get_ip(request)
        qs                = product.objects.get(view_by__iexact=view_by).exist()
        if not qs:
        #increament product views
            product.update(views=F('views')+1)
            product.save()
        else: pass
    except: pass
    template_name = 'pervasive/adclass/products/single_product.html'
    context               = {
        'product'             : product,
    }
    return render(request, template_name, context)

def remote_product(request, location=None):
    product = list()
    try:
        product               = Postproduct.objects.filter(active=True).filter(location='remote').all()
        '''model manager function with ip address META option'''
    except: pass
    template_name = 'products/adclass/product_filter.html'
    context = {
        'product': product,
    }

    return render(request, template_name, context)

def filter_product_type(request, product_type=None):
    product = list()
    try:
        product               = Postproduct.objects.filter(product_type=product_type)
        '''' Record the last accessed date and number of view'''
        product.last_accessed = timezone.now()
        '''model manager function with ip address META option'''
        #product.increament
        product.last_accessed = timezone.now()
        product.save()
    except: pass
    context = {
        'product': product,
    }
    return render(request, 'products/adclass/product_filter.html', context)





'''
                                   For Clients(User)
                    The views below are indented to only be used by site
                            visitors that aren't logged in
'''

class ProductView(TemplateView):
    template_name = 'profiles/adclass/products/all_products.html'

    def get(self, request, user =None):
        product                 = Product.objects.filter(user=request.user).filter(active=True).filter(deleted=False)
        context             = {
            "title": 'Products',
            'product': product,
        }
        return render(request, self.template_name, context)

'''
this line below are only views for the logged in user
'''
@login_required
def add_product(request):
    template_name = 'profiles/adclass/products/add_product.html'
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        return redirect('products:ProductView')
        print(form.errors)
    else:
        form = ProductForm(request.POST or None, request.FILES or None)

    context = {
        'form': form,
        "title": 'Products | add',
    }
    return render(request, template_name, context)


@require_http_methods(['GET'])
def search(request):
    query                               = request.GET.get('q')
    context                             = list()
    if query:
        object_list = Product.objects.active().filter(
                Q(product_icontains         = query)|
                Q(country__icontains    = query) |
                Q(city__icontains       = query)|
                Q(user__icontains       = query)|
                Q(product_type__icontains   = query)
                ).distinct().order_by('-created')
        template_name = 'profiles/adclass/products/product_search.html'
        context                         ={
            'object_list': object_list,
            'query': query
        }
        return render(request, template_name, context)
    return HttpResponse('Please type something.')

@login_required
def corp_all_product_view(request):
    product                 = Product.objects.active()
    template_name = 'profiles/adclass/products/all_products.html'
    context = {
        'product': product,
        'title': 'products',
    }
    return render(request, template_name, context)
 
@login_required
def corp_single_product_view(request, slug=None):
    product                 = get_object_or_404(Product, slug=slug)
    template_name       = 'profiles/adclass/products/single_product_corp.html'
    context = {
        'product': product,
    }
    return render(request, template_name, context)

@login_required
def delete_product(request, slug=None):
    product             = get_object_or_404(Product, slug=slug)
    product.deleted     = True
    product.active      = False
    product.save()
    return redirect("products:ProductView")

@login_required
def restore_product(request, slug=None):
    product             = get_object_or_404(Product, slug=slug)
    product.deleted     = False
    product.active      = True
    product.save()
    return redirect("products:ProductView")

@login_required
def delete_product_permanent(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    product.delete()
    product.save()
    return redirect("products:ProductView")

@login_required
def update_product(request, slug=None):
    product = get_object_or_404(Product, slug=slug)
    template_name = 'profiles/adclass/products/edit_product.html'
    form = UpdateProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        product = form.save(commit=False)
        product.edited = True
        product.last_edited = timezone.now()
        product.save()
        #messages.success(request, 'The product was successfully updated!')
        return redirect(reverse('products:corp_single_product_view', kwargs={'slug': product.slug}))
    else:
        form = UpdateProductForm(request.POST or None, request.FILES or None, instance=product)
        #messages.error(request, 'Please the correct errors below!')

    context = {
    "title": product.product_tittle,
    "product": product,
    "form":form,
    }
    return render(request, template_name, context)
