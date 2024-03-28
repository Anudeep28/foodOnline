from django.contrib import admin

from marketplace.models import cartModel

# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'updated_at',)

admin.site.register(cartModel, cartAdmin)