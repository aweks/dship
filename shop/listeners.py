from django.db.models import signals
from dropship.shop.handlers import extended_profile_handler

def start_listeners():
    signals.post_save.connect(extended_profile_handler)
