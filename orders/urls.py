from django.urls import path

from orders import views


app_name='orders'

urlpatterns = [

    # checkout page
    path('checkout/', views.checkoutView, name='checkout'),
    # Place order page after checkout
    path('placeOrder/', views.placeOrderView, name='placeOrder'),
    # After successful transaction of payment
    path('payments/', views.paymentsView, name='payments')

]