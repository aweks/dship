from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^cart/$', 'dropship.shop.views.cart.cart'),
    (r'^order/$', 'dropship.shop.views.order.index'),
    (r'^order/(?P<order_id>\d+)/$', 'dropship.shop.views.order.order_by_id'),
    (r'^order/complete/(?P<order_id>\d+)/$', 'dropship.shop.views.order.complete'),
    (r'^order/tracking/(?P<user_id>\d+)/$', 'dropship.shop.views.order.order_tracking'),
    (r'^order/tracking/admin/$', 'dropship.shop.views.admin_tracking.admin_order_tracking'),
    (r'^edit/shippingaddress/(?P<item_id>\d+)/$', 'dropship.shop.views.address.ship_edit'),
    (r'^edit/billingaddress/(?P<user_id>\d+)/$', 'dropship.shop.views.address.bill_edit'),
)
