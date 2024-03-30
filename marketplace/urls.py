from django.urls import path

from marketplace import views

app_name='marketplace'

urlpatterns = [

    # Initial page
    path('', views.marketPlaceView, name='marketPlaceView'),

    # Search Path restaurant
    path('restaurantSearch/', views.restaurantSearch, name='restaurantSearch'), # type: ignore

    # Menu
    path('menu/<slug:vendor_slug>/', views.restaurantMenu, name='restaurantMenu'),

    # Add to cart
    path('addToCart/<int:food_id>/', views.addToCart, name='addToCart'),

    # DEcrese the cart quantity
    path('decreaseToCart/<int:food_id>/', views.decreaseToCart, name='decreaseToCart'), # type: ignore

    # Cart page view
    path('cartView/', views.cartView, name='cartView'), # type: ignore

    # delete cart item
    path('deleteCart/<int:cart_id>/', views.deleteCart, name='deleteCart'),    
    


]