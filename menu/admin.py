from django.contrib import admin

from menu.models import CategoryModel, FoodItemModel


# admin class
class CategoryAdmin(admin.ModelAdmin):
    # to prepopulate the cslug field
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at',)
    search_fields = ('category_name', 'vendor__vendor_name',)   

class FoodItemAdmin(admin.ModelAdmin):
    # to prepopulate the cslug field
    prepopulated_fields = {'slug':('food_title',)}
    list_display = ('food_title', 'category','vendor', 'price', 'is_available', 'updated_at',)
    search_fields = ('food_title', 'category__category_name','vendor__vendor_name','price',)
    list_filter =  ('is_available',)
# Register your models here.
admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(FoodItemModel, FoodItemAdmin)