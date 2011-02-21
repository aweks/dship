from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from dropship.products.models import Product, Category, Photo
from dropship.shop.models import Cart
from dropship.products.forms import ProductForm
import os, zipfile, tempfile

import logging

def product_by_id(request, category_id, product_id):
    # first we check to see if this was a submitted form
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # the form is valid so we clean the data and then add it to
            # the cart
            quantity = form.cleaned_data['quantity']

            # we set the other_cost to 0 here because we want to set it
            # directly in the shopping cart rather than the product page
            other_cost = 0

            try:
                user = User.objects.get(id__exact=request.user.id)
            except User.DoesNotExist:
                raise Http404

            # now add the product to the cart - raise a signal?
            cart = Cart.objects.from_request(request)
            cart.add_item(user, product_id, quantity, dict(form.cleaned_data),
                    other_cost)

            return HttpResponseRedirect("/shop/cart/")
    else:
        form = ProductForm()

    # --------------------------------------------------------------------
    try:
        prod = Product.objects.get(id__exact=product_id)
        cate = Category.objects.get(id__exact=category_id)
    except Product.DoesNotExist, Category.DoesNotExist:
        raise Http404

    try:
        images = Photo.objects.filter(product__exact=prod)
    except Photo.DoesNotExist:
        pass

    return render_to_response('products/product.html',
                              {'product': prod,
                               'category': cate,
                               'images': images,
                               'form': form},
                              context_instance=RequestContext(request))

@login_required
def download_product_images(request, product_id):
    """Downloads all the photos related to a specified product in a zip
    archive.
    """
    temp = tempfile.TemporaryFile()
    # append datetime.utcnow() to the end of the filename to avoid conflicts
    photo_zip = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    try:
        product_images = Photo.objects.filter(product__exact=product_id)
    except ProductImage.DoesNotExist:
        raise Http404

    for image in product_images:
        head, tail = os.path.split(image.original_image.path)
        os.chdir(head)
        photo_zip.write(tail)

    wrapper = FileWrapper(temp)
    photo_zip.close()

    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=images.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response
