from accounts.validators import check_images
from .models import CategoryModel, FoodItemModel
from django import forms

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['category_name', 'description',]


class FoodItemModelForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}), validators=[check_images])
    class Meta:
        model = FoodItemModel
        fields = ['category', 'food_title', 'description', 'price', 'image', 'is_available', ]
