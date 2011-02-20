from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _

class ProductForm(forms.Form):
    quantity = forms.IntegerField(label=_("Quantity"), initial=1)
    addressee = forms.CharField(label=_("Full Name"))
    address_one = forms.CharField(label=_("Address One"))
    address_two = forms.CharField(label=_("Address Two"), required=False)
    city = forms.CharField(label=_("City"))
    state = forms.CharField(label=_("State"), required=False)
    post_code = forms.CharField(label=_("Post Code"))
    email = forms.EmailField(label=_("Email"), required=False)
