from django.urls import path

from customers import views


app_name='customers'

urlpatterns = [

    # Initial page
    path('profile/', views.customerProfile, name='profile'),

]