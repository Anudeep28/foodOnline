from django.db import models
from django.urls import path
from . import views

app_name='vendor'

urlpatterns = [
    # register vendor
    path('vendorRegister/', views.vendorRegisterView , name='vendorRegister'),
    

]


