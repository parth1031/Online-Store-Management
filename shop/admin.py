from django.contrib import admin
from .models import Customers, Products,cart,cartitems

# Register your models here.

admin.site.register(Products)
admin.site.register(Customers)
admin.site.register(cart)
admin.site.register(cartitems)




