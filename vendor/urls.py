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
    
    #  Menu Builder
    path('menuBuilder/', views.menuBuilder, name = 'menuBuilder'),
    path('menuBuilder/category/<int:pk>/', views.menuBuilderCategory, name = 'menuBuilderCategory'),

    # Category CRUD Edit and delete Category
    path('menuBuilder/category/add', views.addCategory, name='addCategory'),
    path('menuBuilder/category/edit/<int:pk>/', views.editCategory, name='editCategory'),
    path('menuBuilder/category/delete/<int:pk>/', views.deleteCategory, name='deleteCategory'),
    
]


