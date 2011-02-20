from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
import os

DIRNAME = os.path.dirname(__file__)

admin.autodiscover()

urlpatterns = patterns('',
    # TODO remove this before going into production!
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DIRNAME, 'static')}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DIRNAME, 'media')}),

    # tempory url for testing
    # TODO remove!!
    (r'^$', 'dropship.products.views.category.categories'),

    (r'^accounts/', include('registration.urls')),

    (r'^shop/', include('dropship.shop.urls')),
    (r'^product/', include('dropship.products.urls')),
    # the shipping and payment urls are just commented out here as they have no
    # views associated with them but they may in the future
    #(r'^shipping/', include('dropship.shipping.urls')),
    #(r'^payment/', include('dropship.payment.urls')),

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

# static direct to template urls go here:
urlpatterns += patterns('',
    (r'^about/$', direct_to_template, {'template': 'static/about.html'}),
    (r'^contact/$', direct_to_template, {'template': 'static/contact.html'}),
    (r'^privacy/$', direct_to_template, {'template': 'static/privacy.html'}),
    (r'^terms/$', direct_to_template, {'template': 'static/terms.html'}),
)
