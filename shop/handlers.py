from django.conf import settings
from django.contrib.auth.models import User
from dropship.shop.models import ExtendedProfile
from decimal import Decimal

def extended_profile_handler(sender, instance=None, created=None, **kwargs):
    if isinstance(instance, User) and created:
        # we now need to make sure that the instance has profile associated
        # with it and if not we need to create one
        try:
            # we try to retrieve a profile and if it exists we simply
            # continue
            profile = ExtendedProfile.objects.get(id__exact=instance.id)
        except ExtendedProfile.DoesNotExist:
            # since the profile does not exist we create one
            profile = ExtendedProfile(user=instance,
                            billing=None,
                            # commission_rate=settings.DEFAULT_COMMISSION_RATE)
                            commission_rate=Decimal(str(settings.DEFAULT_COMMISSION_RATE)))
            profile.save()
