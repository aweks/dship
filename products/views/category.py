from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from dropship.products.models import Product, Category
from dropship.products.forms import ProductForm

import logging

def categories(request):
    try:
        cates = Category.objects.all()
    except Category.DoesNotExist:
        raise Http404

    return render_to_response('products/all_categories.html',
                              {'categories': cates},
                              context_instance=RequestContext(request))

def category_by_id(request, category_id):
    try:
        prods = Product.objects.filter(stock__gt=0) \
                               .filter(category__exact=category_id)
        cate = Category.objects.get(id__exact=category_id)
    except Product.DoesNotExist, Category.DoesNotExist:
        raise Http404

    return render_to_response('products/products_in_category.html',
                              {'products': prods, 'category': cate},
                              context_instance=RequestContext(request))
