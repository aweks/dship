from django.db import models
from decimal import Decimal

class CurrencyField(models.DecimalField):
    """Provides a CurrencyField for Django models.
    Takes two arguments: max_digits and decimal_places."""
    __metaclass__ = models.SubfieldBase

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
           return None
