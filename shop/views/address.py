from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dropship.shop.models import ShippingAddress, BillingAddress, Cart, CartItem
from dropship.shop.forms import ShippingAddressForm, BillingAddressForm

@login_required
def ship_edit(request, item_id):
    """Rather than just editing a specific address it should create a new
    address and then use the already existing mechanism to check the database
    to see if it already exists. If it does then it simply updates the CartItem
    with that address and if not then it adds a new address to the database.
    """
    # get the cart item and cart details here so we can use them even if the
    # form is invalid
    try:
        cartitem = CartItem.objects.get(id__exact=item_id)
        cart = Cart.objects.get(id__exact=cartitem.cart.id)
    except CartItem.DoesNotExist, Cart.DoesNotExist:
        return Http404

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            if int(request.user.id) != int(cart.customer.id):
                raise Http404

            # first we see if we can find the address and if we can we return
            # that, if not we add it to the database, save the address and then
            # return that
            cartitem.address = cart.find_ship_address(form.cleaned_data)
            cartitem.save()

            return HttpResponseRedirect('/shop/cart/')

    form = ShippingAddressForm()
    return render_to_response('shop/shipping_addr.html',
                              {'form': form,
                               'cartitem': cartitem,
                               'cart': cart},
                              context_instance=RequestContext(request))

@login_required
def bill_edit(request, user_id):
    if request.method == 'POST':
        form = BillingAddressForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(id__exact=user_id)
                profile = user.get_profile()
            except User.DoesNotExist:
                raise Http404

            if int(request.user.id) != int(user.id):
                raise Http404

            try:
                if profile.billing:
                    profile.billing.delete()
            except BillingAddress.DoesNotExist:
                pass

            bill_addr = BillingAddress.objects.add_billing_address(
                            addressee=form.cleaned_data['addressee'],
                            address_one=form.cleaned_data['address_one'],
                            address_two=form.cleaned_data['address_two'],
                            city=form.cleaned_data['city'],
                            state=form.cleaned_data['state'],
                            post_code=form.cleaned_data['post_code'])

            profile.billing = bill_addr
            profile.save()

            return HttpResponseRedirect('/shop/order/')

    form = BillingAddressForm()

    return render_to_response('shop/billing_addr.html',
                              {'form': form,
                               'user_id': user_id},
                              context_instance=RequestContext(request))
