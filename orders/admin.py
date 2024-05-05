from django.contrib import admin
from orders.models import PaymentModel, OrderModel, OrderedFoodModel
# Register your models here.

class orderedFoodInline(admin.TabularInline):
    model = OrderedFoodModel
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')

class orderAdmin(admin.ModelAdmin):
    list_displays = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status', 'is_ordered']
    inlines =  [orderedFoodInline]

admin.site.register(PaymentModel)
admin.site.register(OrderModel, orderAdmin)
admin.site.register(OrderedFoodModel)