from django.contrib import admin

from marketplace.models import cartModel, taxModel

# Register your models here.

class cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'food_item', 'quantity', 'updated_at',)

class taxModelAdmin(admin.ModelAdmin):
    list_display = ('tax_type', 'tax_percentage', 'is_active',)

admin.site.register(cartModel, cartAdmin)
admin.site.register(taxModel, taxModelAdmin)