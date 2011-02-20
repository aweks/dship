from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf import settings
from decimal import Decimal
from dropship.products import fields
from dropship.products.models import Product
from dropship.shop.exceptions import InvalidItemOptionsException, NoAddressSpecifiedException

import logging
logger = logging.getLogger('dropship'+__name__)

from south.modelsinspector import add_introspection_rules
add_introspection_rules(
        [],
        ["^dropship\.products\.fields\.CurrencyField"]
)

class CartManager(models.Manager):
    """Deals with creating or retrieving the Cart from a request.
    First it checks with to see if the request contains an already
    existing cart in the session. If it does then it simply gets cart
    id and retrives the data from the database. If it does not then it
    just creates a new cart object and sets the session appropriately."""

    def from_request(self, request):
        try:
            user = User.objects.get(id__exact=request.user.id)
        except User.DoesNotExist:
            user = None
        if 'cart' in request.session:
            # cart already exists
            cart_id = request.session['cart']

            try:
                # find the cart
                cart = Cart.objects.get(id__exact=cart_id)
            except Cart.DoesNotExist:
                # if it doen't exist make a new one and associate that
                # one with the session
                if request.user:
                    cart = Cart(customer=user, total=0)
                    cart.save()
                else:
                    cart = Cart(total=0)
                    cart.save()
                request.session['cart'] = cart.id
            return cart
        else:
            # no cart found in the session so we just create one
            if request.user:
                cart = Cart(customer=user, total=0)
                cart.save()
            else:
                cart = Cart(total=0)
                cart.save()
            request.session['cart'] = cart.id
            return cart

class Cart(models.Model):
    customer = models.ForeignKey(User, verbose_name=_(u'Cart Owner'))
    date_created = models.DateTimeField(auto_now_add=True,
            verbose_name=_(u'Creation Date'))
    total = fields.CurrencyField(max_digits=19, decimal_places=2,
            verbose_name=_(u'Cart Total'))

    objects = CartManager()

    class Meta:
        verbose_name = _(u'Shopping Cart')
        verbose_name_plural = _(u'Shopping Carts')

    # TODO
    # safe to remove the user argument
    def add_item(self, user=None, product_id=None, quantity=None,
            address=None, other_cost=None):
        """Adds an item to the cart."""
        if not product_id or not quantity or not address:
            raise InvalidItemOptionsException
        else:
            # add the item to the cart
            addr = self.find_ship_address(address)

            prod = Product.objects.get(id__exact=product_id)
            cartitem = CartItem(cart=self, item=prod, price=prod.price,
                            address=addr, quantity=quantity,
                            other_cost=other_cost,
                            total=0)

            cartitem.update_total()
            self.update_total()

            cartitem.save()
            self.save()

    def update_total(self):
        """Like the update_total method in the CartItem class this simply
        reworks out the cart total when called."""
        cartitems = CartItem.objects.filter(cart__exact=self)
        total = Decimal(0)
        for item in cartitems:
            total += item.total

        self.total = total
        self.save()

    def find_ship_address(self, address=None):
        """Simply takes an address in dict form and either returns the address
        object if it was found, or if the address does NOT exist it creates it
        and then returns the newly created object instead
        """
        if not address:
            # make sure the address has actually been passed in
            raise NoAddressSpecifiedException
        else:
            # find out if the address already exists in the db
            addr_set = ShippingAddress.objects.filter(addressee__exact=address['addressee']) \
                                .filter(address_one__exact=address['address_one']) \
                                .filter(address_two__exact=address['address_two']) \
                                .filter(city__exact=address['city']) \
                                .filter(state__exact=address['state']) \
                                .filter(post_code__exact=address['post_code']) \
                                .filter(email__exact=address['email'])
            if not addr_set:
                # if it doesn't then we add it
                try:
                    addr = ShippingAddress(addressee=address['addressee'],
                                       address_one=address['address_one'],
                                       address_two=address['address_two'],
                                       city=address['city'],
                                       state=address['state'],
                                       post_code=address['post_code'],
                                       email=address['email'])
                    addr.save()
                except Exception:
                    logger.debug('Unable to create a new address object in '+__name__)
            else:
                # because a filter query returns a queryset we need to do this
                # becase the rest of the code expects a single address to be
                # returned - if it returned None then that also works as we just
                # create a new address in the next part anyway - otherwise we just
                # return this value as is
                addr = addr_set[0]
        return addr

class BillingAddressManager(models.Manager):
    def add_billing_address(self, addressee=None, address_one=None,
                                         address_two=None, city=None,
                                         state=None, post_code=None,
                                         email=None):
        """Finds out if a given billing address already exists in the database.
        If it does then it returns it, if not then it saves it in the database
        and then returns that.
        """
        # find out if the address already exists in the db
        addr_set = BillingAddress.objects.filter(addressee__exact=addressee) \
                                .filter(address_one__exact=address_one) \
                                .filter(address_two__exact=address_two) \
                                .filter(city__exact=city) \
                                .filter(state__exact=state) \
                                .filter(post_code__exact=post_code)
        if not addr_set:
            # if it doesn't then we add it
            try:
                addr = BillingAddress(addressee=addressee,
                                   address_one=address_one,
                                   address_two=address_two,
                                   city=city,
                                   state=state,
                                   post_code=post_code)
                addr.save()
            except Exception:
                logger.debug('Unable to create a new address object in '+__name__)
        else:
            # because a filter query returns a queryset we need to do this
            # becase the rest of the code expects a single address to be
            # returned - if it returned None then that also works as we just
            # create a new address in the next part anyway - otherwise we just
            # return this value as is
            addr = addr_set[0]
        return addr

class BillingAddress(models.Model):
    addressee = models.CharField(max_length=80)
    address_one = models.CharField(max_length=80)
    address_two = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    post_code = models.CharField(max_length=30)

    objects = BillingAddressManager()

    def __unicode__(self):
        return self.addressee + ' ' + self.city

class ShippingAddress(models.Model):
    addressee = models.CharField(max_length=80)
    address_one = models.CharField(max_length=80)
    address_two = models.CharField(max_length=80, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    post_code = models.CharField(max_length=30)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.addressee + ' ' + self.city

class CartItem(models.Model):
    cart = models.ForeignKey(Cart)
    item = models.ForeignKey(Product)
    price = fields.CurrencyField(max_digits=19, decimal_places=2)
    address = models.ForeignKey(ShippingAddress)
    quantity = models.BigIntegerField()
    other_cost = fields.CurrencyField(max_digits=19, decimal_places=2,
            blank=True, null=True)
    total = fields.CurrencyField(max_digits=19, decimal_places=2)

    def __get_commission_rate(self):
        try:
            user = User.objects.get(id__exact=self.cart.customer.id)
        except User.DoesNotExist:
            raise Http404

        try:
            profile = user.get_profile()
            if profile.commission_rate:
                return user.commission
            else:
                return settings.DEFAULT_COMMISSION_RATE
        except ExtendedProfile.DoesNotExist, BillingAddress.DoesNotExist:
            return settings.DEFAULT_COMMISSION_RATE

    def update_total(self):
        """The update_total method is designed to get the total for an
        item from all known parameters. Before it saves the price to the db it
        first checks to make sure that the options fall within acceptable
        values. If they do not then it does not save the data to the database.
        """
        total = Decimal(0)
        total = Decimal(self.price) * int(self.quantity)
        total -= Decimal(self.other_cost)
        total -= Decimal(str(self.__get_commission_rate()))
        self.total = total
        if self.check_price_correct():
            self.save()
            return True
        else:
            return False

    def check_price_correct(self):
        """We use this to ensure that the price of a CartItem is valid."""
        if self.total > 0 and \
            (self.price - Decimal(str(self.__get_commission_rate()))) > self.other_cost and \
            self.price > Decimal(str(self.__get_commission_rate())):
            return True
        else:
            return False

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('SNT', _('Dispatched')),
        ('DSP', _('Dispatching')),
        ('PRC', _('Processing')),
    )

    customer = models.ForeignKey(User)
    billing = models.ForeignKey(BillingAddress)
    status = models.CharField(max_length=3, choices=ORDER_STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    total = fields.CurrencyField(max_digits=19, decimal_places=2)

    def __unicode__(self):
        return 'ID:' + ' ' + str(self.id) + ' Customer: ' + \
                self.customer.username

    class Meta:
        verbose_name = _(u'Order')
        verbose_name_plural = _(u'Orders')

    def add_item(self, cartitem=None):
        """Adds an item to an order."""
        # make sure that cartitem is not None and that it is actually an
        # instance of CartItem
        if not cartitem or not isinstance(cartitem, CartItem):
            raise InvalidItemOptionsException
        else:
            orderitem = OrderItem(order=self, item=cartitem.item,
                    address=cartitem.address, price=cartitem.price,
                    quantity=cartitem.quantity, other_cost=cartitem.other_cost,
                    total=cartitem.total)
            orderitem.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order)
    item = models.ForeignKey(Product)
    price = fields.CurrencyField(max_digits=19, decimal_places=2)
    address = models.ForeignKey(ShippingAddress)
    quantity = models.BigIntegerField()
    other_cost = fields.CurrencyField(max_digits=19, decimal_places=2,
            blank=True, null=True)
    total = fields.CurrencyField(max_digits=19, decimal_places=2)

class ExtendedProfile(models.Model):
    user = models.OneToOneField(User)
    billing = models.ForeignKey(BillingAddress, blank=True, null=True)
    commission_rate = fields.CurrencyField(max_digits=19, decimal_places=2,
            blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = _(u'Extended User Information')
        verbose_name_plural = _(u'Extended User Information')
