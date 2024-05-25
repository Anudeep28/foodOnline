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

    # Opening Hours url
    path('openingHours/', views.openingHours, name = 'openingHours'),
    path('addOpeningHours/', views.addOpeningHours, name = 'addOpeningHours'), # type: ignore
    path('deleteOpeningHours/<int:pk>/', views.deleteOpeningHours, name = 'deleteOpeningHours'), # type: ignore
    

    # Category CRUD Edit and delete Category
    path('menuBuilder/category/add', views.addCategory, name='addCategory'),
    path('menuBuilder/category/edit/<int:pk>/', views.editCategory, name='editCategory'),
    path('menuBuilder/category/delete/<int:pk>/', views.deleteCategory, name='deleteCategory'),

    # Food Item CRUD Edit and delete Category
    path('menuBuilder/food/add', views.addFood, name='addFood'),
    path('menuBuilder/food/edit/<int:pk>/', views.editFood, name='editFood'),
    path('menuBuilder/food/delete/<int:pk>/', views.deleteFood, name='deleteFood'),

    # Order Details view
    path('orderDetails/<int:order_number>/', views.orderDetailsView, name='orderDetails'),
    

]


