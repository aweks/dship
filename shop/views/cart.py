from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from dropship.shop.models import Cart, CartItem
from dropship.shop.forms import CartUpdateItemForm

import logging
import logging.handlers

dropship_logger = logging.getLogger('views_cart_logger')
dropship_logger.setLevel(logging.DEBUG)
dropship_handler = logging.handlers.RotatingFileHandler(
              settings.DROPSHIP_LOG_FILE, maxBytes=4096, backupCount=5)
dropship_logger.addHandler(dropship_handler)

@login_required
def cart(request):
    if request.method == 'POST':
        # if the checkout button on the cart page is clicked and the cart name
        # variable is set on the POST request then we just redirect to the next
        # stage of the order process
        if request.POST.has_key('cart'):
            return HttpResponseRedirect('/shop/order/')
        else:
            form = CartUpdateItemForm(request.POST)
            if form.is_valid():
                # cart item update
                try:
                    item = CartItem.objects.get(id__exact=form.cleaned_data['item'])
                    cart = Cart.objects.get(id__exact=item.cart.id)
                except CartItem.DoesNotExist, Cart.DoesNotExist:
                    raise Http404

                if form.cleaned_data['quantity'] == 0:
                    # since the quantity has been set to 0 we delete the item
                    # instead
                    item.delete()
                    cart.update_total()
                    HttpResponseRedirect('/shop/cart/')

                item.price = form.cleaned_data['price']
                item.quantity = form.cleaned_data['quantity']
                item.other_cost = form.cleaned_data['other_cost']
                if item.update_total():
                    cart.update_total()
                    return HttpResponseRedirect('/shop/cart/')
                else:
                    # TODO
                    # on redirect here we need to put a validation error on the
                    # price field of the form to let the user know what the
                    # problem is (otherwise they will have no idea what went
                    # wrong)
                    HttpResponseRedirect('/shop/cart/')

    form = CartUpdateItemForm()
    cart = Cart.objects.from_request(request)
    cartitems = CartItem.objects.filter(cart__exact=cart.id)
    if not cart:
        # we raise an exception here because the cart should be created
        # in the from_request() method above. If it is not something has
        # gone seriously wrong
        dropship_logger.critical('dropship.products.views.cart.cart failed'+
                    ' to get or create a Cart object. Raising Http404.')

    return render_to_response('shop/cart.html',
                              {'cart': cart,
                               'cartitems': cartitems,
                               'form': form},
                              context_instance=RequestContext(request))
