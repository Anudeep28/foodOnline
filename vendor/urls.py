from django.db import models
from django.urls import path
from . import views
from accounts import views as accountViews

app_name='vendor'

urlpatterns = [

    # Initial page
    path('', accountViews.restaurantDashboard, name='restaurant'),
    # register vendor
    path('vendorRegister/', views.vendorRegisterView , name='vendorRegister'),

    # My restaurant profile path
    path('restaurantProfile/', views.restaurantProfile, name ='restaurantProfile'),
    

]


