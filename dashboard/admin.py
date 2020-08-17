from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Paymentmethod)
admin.site.register(Shipping_company)
admin.site.register(Supplier)
admin.site.register(Tag)