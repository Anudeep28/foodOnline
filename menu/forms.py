from .models import CategoryModel, FoodItemModel
from django import forms

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = CategoryModel
        fields = ['category_name', 'description',]