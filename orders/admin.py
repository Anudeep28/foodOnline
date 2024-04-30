from django.contrib import admin
from orders.models import PaymentModel, OrderModel, OrderedFoodModel
# Register your models here.
admin.site.register(PaymentModel)
admin.site.register(OrderModel)
admin.site.register(OrderedFoodModel)