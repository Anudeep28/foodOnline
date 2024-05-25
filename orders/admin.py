from django.contrib import admin
from orders.models import PaymentModel, OrderModel, OrderedFoodModel
# Register your models here.

class orderedFoodInline(admin.TabularInline):
    model = OrderedFoodModel
    readonly_fields = ('order', 'payment', 'user', 'fooditem', 'quantity', 'price', 'amount')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone', 'email', 'total', 'payment_method', 'status','order_placed_to', 'is_ordered']
    inlines =  [orderedFoodInline]

admin.site.register(PaymentModel)
admin.site.register(OrderModel, OrderAdmin)
admin.site.register(OrderedFoodModel)