from django.contrib import admin

from vendor.models import Vendor, openingHoursModel




class VendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','is_approved', 'created_at')
    # when i click onthe user or vendor we will get directed to it
    list_display_links = ('user','vendor_name')

class openingHoursModelAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'day', 'from_hours', 'to_hours',)
# Register your models here.
admin.site.register(Vendor,VendorAdmin)
admin.site.register(openingHoursModel, openingHoursModelAdmin)