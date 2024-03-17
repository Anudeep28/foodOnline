from django import forms

from vendor.models import Vendor

# custom validations
from accounts.validators import check_images

class VendorForm(forms.ModelForm):
    vendor_lincense = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[check_images])
    class Meta:
        model = Vendor
        fields = ['vendor_name', 'vendor_lincense']