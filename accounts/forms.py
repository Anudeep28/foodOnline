from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import User, UserProfile
from .validators import check_images

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'phone_number',
                  'password']
        
    # how to validate the password and confirm password equal
        # this is shown in the html tag
    def clean(self):
        cleaned_data = super(CustomUserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords does not match")
        

class UserProfileForm(forms.ModelForm):
    # adding our custom validator here in forms
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing...','required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[check_images])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}), validators=[check_images])

    # Making readonly fields
    # the other way is given below
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pincode', 'longitude', 'latitude')

    # the other way to do things
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs) 
        for field in self.fields:
            if field in ['latitude','longitude']:
                self.fields[field].widget.attrs['readonly'] = 'readonly'       