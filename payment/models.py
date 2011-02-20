from django.db import models
from dropship.shop.listeners import start_listeners

# start all signal listerners
start_listeners()