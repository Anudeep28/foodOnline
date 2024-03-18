from django.urls import path

app_name='menu'

urlpatterns = [

    # Initial page
    path('', accountViews.restaurantDashboard, name='restaurant'),
    # register vendor
    path('vendorRegister/', views.vendorRegisterView , name='vendorRegister'),

    # My restaurant profile path
    path('restaurantProfile/', views.restaurantProfile, name ='restaurantProfile'),
    

]