from django.urls import path

from orders import views


app_name='orders'

urlpatterns = [

    # Initial page
    path('', views.checkoutView, name='checkout'),

]