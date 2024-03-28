from ast import Delete
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from marketplace.context_processors import get_cart_amount, get_cart_counter
from marketplace.models import cartModel
from menu.models import CategoryModel, FoodItemModel
from vendor.models import Vendor

# Reverse fetch
from django.db.models import Prefetch
# decorator
from django.contrib.auth.decorators import login_required

# Create your views here.




def marketPlaceView(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    # to avoid exposing the model to html we create context
    vendors_count = vendors.count()
    context = {
        "vendors":vendors,
        "vendors_count":vendors_count
    }
    return render(request, 'marketplace/listings.html', context)


def restaurantMenu(request, vendor_slug):
    restaurant = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    """# Reverse look up example below we have from category to food item fetching"""
    categories = CategoryModel.objects.filter(vendor=restaurant).prefetch_related(
        Prefetch(
            'fooditemmodel',
            queryset=FoodItemModel.objects.filter(is_available=True)
        )
    )
    # To get the cart details of the user
    if request.user.is_authenticated:
        cart_items = cartModel.objects.filter(user=request.user)
    else:
        cart_items = None
    
    # Now the category context has fooditems as well as categorie sin it 
    # it is accessible by category.fooditemmodel
    context = {
        "restaurant":restaurant,
        "categories":categories,
        "cart_items":cart_items
    }

    return render(request, 'marketplace/restaurantMenu.html', context)


def addToCart(request, food_id=None):
    """The status response is used in the java script for doinf some conditions"""
    if request.user.is_authenticated:
        # this is for ajax request or response need to figure it out ?
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                foodItem = FoodItemModel.objects.get(id=food_id)
                # Check if user have already added food to the cart
                try:
                    checkCart = cartModel.objects.get(user=request.user, food_item = foodItem )
                    # Increase the crat quantity
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status':'Success','message':'Increased cart quantity', 
                                         'cart_count':get_cart_counter(request), 
                                         'quantity':checkCart.quantity,
                                         'cart_amount':get_cart_amount(request)})
                except:
                    checkCart = cartModel.objects.create(user=request.user, food_item = foodItem, quantity = 1)
                    return JsonResponse({'status':'Success','message':'Added the food item',
                                          'cart_count':get_cart_counter(request), 
                                          'quantity':checkCart.quantity,
                                         'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status':'Failed',
                                     'message':'This food item does not exist'})
        else:
            return JsonResponse({'status':'Failed',
                                 'message':'Please Login to Continue!'})
    else:
        return JsonResponse({'status':'login_required',
                             'message':'Please Login to Continue!'})
    

def decreaseToCart(request, food_id=None):
    if request.user.is_authenticated:
        # this is for ajax request or response need to figure it out ?
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                foodItem = FoodItemModel.objects.get(id=food_id)
                # Check if user have already added food to the cart
                try:
                    checkCart = cartModel.objects.get(user=request.user, food_item = foodItem )
                    # Decrease the cart quantity
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                    else:
                        try:
                            checkCart.delete()
                        except:
                            checkCart.quantity = 0        
                        checkCart.quantity = 0
                    return JsonResponse({'status':'Success','message':'Decreased cart quantity',
                                          'cart_count':get_cart_counter(request), 
                                          'quantity':checkCart.quantity,
                                         'cart_amount':get_cart_amount(request)})
                except:
                    return JsonResponse({'status':'Failed','message':'You do not have this item in your cart'})
            except:
                return JsonResponse({'status':'Failed','message':'This food item does not exist'})
        else:
            return JsonResponse({'status':'Failed','message':'Please Login to Continue!'})
    else:
        return JsonResponse({'status':'login_required','message':'Please Login to Continue!'})
    

    
@login_required(login_url='accounts:userLogin')
def cartView(request):
    cart_items = cartModel.objects.filter(user=request.user).order_by('created_at')
    context = {
        "cart_items":cart_items
    }
    return render(request, 'marketplace/cartView.html', context)


def deleteCart(request, cart_id):
    # handling this by AJAX 
    if request.user.is_authenticated:
        # this is for ajax request or response need to figure it out ?
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # check if the cart item is present or not
                cart_item = cartModel.objects.get(user=request.user, pk=cart_id)
                cart_item.delete()
                return JsonResponse({'status':'Success',
                                     'message':'Cart Item have been delete', 
                                     'cart_count':get_cart_counter(request),
                                    'cart_amount':get_cart_amount(request)})
            except:
                return JsonResponse({'status':'Failed','message':'You do not have this item in your cart'})
        else:
            return JsonResponse({'status':'Failed','message':'Please Login to Continue!'})
    else:
        return JsonResponse({'status':'login_required','message':'Please Login to Continue!'})