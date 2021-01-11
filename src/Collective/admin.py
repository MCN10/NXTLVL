from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(CollectiveCustomer)
admin.site.register(CollectiveProduct)
admin.site.register(CollectiveCategory)
admin.site.register(CollectiveOrder)
admin.site.register(CollectiveOrderItem)
admin.site.register(CollectiveShippingAddress)


