from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

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