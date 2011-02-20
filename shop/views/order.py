from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dropship.shop.forms import OrderCompleteForm
from dropship.shop.models import Cart, CartItem, ExtendedProfile, Order, OrderItem, BillingAddress

import logging
logger = logging.getLogger('dropship'+__name__)

@login_required
def index(request):
    # get the correct info for the rest of the view
    cart = Cart.objects.from_request(request)
    cartitems = CartItem.objects.filter(cart__exact=cart)

    if request.method == 'POST':
        form = OrderCompleteForm(request.POST)
        if form.is_valid():
            try:
                # we try and get the customers profile
                profile = cart.customer.get_profile()
            except ExtendedProfile.DoesNotExist:
                # every user should have a profile so if they don't we raise a
                # 404
                raise Http404
            if profile.billing:
                current_order = Order(
                    customer=cart.customer,
                    billing=profile.billing,
                    status='PRC',
                    total=cart.total)

                current_order.save()

                # now we get all the cart items associated with the cart and
                # turn them into orderitems
                for i in cartitems:
                    current_order.add_item(i)

                # now that the order has been created we are safe to delete the
                # cart and all the cartitems associated with it
                for i in cartitems:
                    i.delete()

                cart.delete()

                return HttpResponseRedirect('/shop/order/complete/'+str(current_order.id)+'/')

            else:
                return HttpResponseRedirect('/shop/edit/billingaddress/'+str(cart.customer.id)+'/')

    form = OrderCompleteForm()
    return render_to_response('order/index.html',
                              {'cart': cart,
                               'cartitems': cartitems,
                               'form': form},
                               context_instance=RequestContext(request))

@login_required
def complete(request, order_id):
    try:
        user = User.objects.get(id__exact=request.user.id)
    except User.DoesNotExist:
        raise Http404

    try:
        order = Order.objects.get(id__exact=order_id)
        orderitems = OrderItem.objects.filter(order__exact=order)
    except Order.DoesNotExist, OrderItem.DoesNotExist:
        # if we get here and the order id is not found then we should just
        # return a 404
        raise Http404

    # if the user accessing the page is not the same user as the one who made
    # the order also return a 404
    if order.customer.id != user.id:
        raise Http404

    return render_to_response('order/complete.html',
                              {'order': order,
                               'user': user,
                               'orderitems': orderitems},
                               context_instance=RequestContext(request))

@login_required
def order_by_id(request, order_id):
    try:
        order = Order.objects.get(id__exact=order_id)
        orderitems = OrderItem.objects.filter(order__exact=order)
    except Order.DoesNotExist, OrderItem.DoesNotExist:
        raise Http404

    if request.user.id != order.customer.id:
        raise Http404

    return render_to_response('order/by_id.html',
                              {'order': order,
                               'orderitems': orderitems},
                              context_instance=RequestContext(request))

@login_required
def order_tracking(request, user_id):
    try:
        user = User.objects.get(id__exact=user_id)
    except User.DoesNotExist:
        raise Http404

    if user.id != int(user_id):
        raise Http404

    try:
        orders = Order.objects.filter(customer__exact=user)
    except Order.DoesNotExist:
        pass

    return render_to_response('order/tracking.html',
                              {'user': user,
                               'orders': orders},
                              context_instance=RequestContext(request))
