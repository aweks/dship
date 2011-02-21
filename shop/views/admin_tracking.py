from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dropship.shop.models import Order

@login_required
def admin_order_tracking(request):
    try:
        user = User.objects.get(id__exact=request.user.id)
    except User.DoesNotExist:
        raise Http404

    if not user.is_superuser:
        raise Http404

    orders = Order.objects.all()

    return render_to_response('order/admin_tracking.html',
                              {'orders': orders},
                              context_instance=RequestContext(request))
