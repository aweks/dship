from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class BillingAddressForm(forms.Form):
    addressee = forms.CharField(label=_("Name"))
    address_one = forms.CharField(label=_("Address One"))
    address_two = forms.CharField(label=_("Address Two"), required=False)
    city = forms.CharField(label=_("City"))
    state = forms.CharField(label=_("State"))
    post_code = forms.CharField(label=_("Post Code"))

class ShippingAddressForm(forms.Form):
    addressee = forms.CharField(label=_("Full Name"))
    address_one = forms.CharField(label=_("Address One"))
    address_two = forms.CharField(label=_("Address Two"), required=False)
    city = forms.CharField(label=_("City"))
    state = forms.CharField(label=_("State"))
    post_code = forms.CharField(label=_("Post Code"))
    email = forms.EmailField(label=_("Email"), required=False)

class CartUpdateItemForm(forms.Form):
    item = forms.IntegerField()
    quantity = forms.IntegerField()
    price = forms.DecimalField(max_digits=19, decimal_places=2)
    other_cost = forms.DecimalField(max_digits=19, decimal_places=2)

class OrderCompleteForm(forms.Form):
    accept = forms.BooleanField(label=_("Accept and Complete Order"))
