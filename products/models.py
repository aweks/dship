from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from imagekit.models import ImageModel
from dropship.products import fields
from dropship.products.exceptions import InvalidImageException

from south.modelsinspector import add_introspection_rules
add_introspection_rules(
        [],
        ["^dropship\.products\.fields\.CurrencyField"]
)

class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = fields.CurrencyField(max_digits=19, decimal_places=2)
    stock = models.BigIntegerField()

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

class Photo(ImageModel):
    name = models.CharField(max_length=100)
    original_image = models.ImageField(upload_to='photos')
    num_views = models.PositiveIntegerField(editable=False, default=0)
    product = models.ForeignKey(Product)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'products.specs'
        cache_dir = 'photos'
        image_field = 'original_image'
        save_count_as = 'num_views'
