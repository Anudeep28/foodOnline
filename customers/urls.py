from django.urls import path

from customers import views


app_name='customers'

urlpatterns = [

    # Initial page
    path('profile/', views.customerProfile, name='profile'),
    # customer dashboard my orders
    path('myOrders/',views.myOrdersView, name='myOrders'),
    # order detail path
    path('OrderDetails/<int:order_number>/', views.OrderDetailsView, name='OrderDetails')

]