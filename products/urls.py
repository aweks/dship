from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # displays all categories
    (r'^all/$', 'dropship.products.views.category.categories'),

    # displays all products in given category (as long as they are in stock)
    (r'^(?P<category_id>\d+)/$', 
        'dropship.products.views.category.category_by_id'),

    # displays a specific product (even if the product is out of stock)
    (r'^(?P<category_id>\d+)/(?P<product_id>\d+)/$',
        'dropship.products.views.product.product_by_id'),

    # allows the download of all images associated with a product as a zip file
    (r'^download/images/(?P<product_id>\d+)/$',
        'dropship.products.views.product.download_product_images'),
)
