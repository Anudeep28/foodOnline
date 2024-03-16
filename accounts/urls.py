from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    
    #App
    path('userRegister/', views.userRegisterView , name='userRegister'),

    # login / logout
    path('userLogin/', views.userLogin , name='userLogin'),
    path('userLogout/', views.userLogout , name='userLogout'),

    # path of url decider
    path('accountDecider/', views.accountDecider, name='accountDecider'),

    # dashboard
    path('dashboard/', views.dashboard , name='dashboard'),
    path('cusDashboard/', views.cusDashboard , name='cusDashboard'),
    path('restaurantDashboard/', views.restaurantDashboard , name='restaurantDashboard'),

    # activation path
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Forgot Password
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password', views.reset_password, name='reset_password'),
    


]