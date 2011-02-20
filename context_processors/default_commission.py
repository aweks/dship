def default_commission_rate(request):
    from django.conf import settings
    return {'default_commission': settings.DEFAULT_COMMISSION_RATE}
