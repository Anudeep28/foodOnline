from django.shortcuts import redirect, render

from accounts.models import UserProfile
from marketplace.models import cartModel
from orders.forms import OrderModelForm
# decorators
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:userLogin')
def checkoutView(request):
    # How to prepopulate the order form
    # the form is the combnation of information from user model and 
    # userprofile model so we can get that information inside the ordermodel
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {'first_name':request.user.first_name,
                      'last_name':request.user.last_name,
                      'phone':request.user.phone_number,
                      'email':request.user.email,
                      'address':user_profile.address,
                      'country':user_profile.country,
                      'city':user_profile.city,
                      'state':user_profile.state,
                      'pin_code':user_profile.pincode,
                      }
    order_form = OrderModelForm(initial=default_values)
    # cart model
    cart_items = cartModel.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace:marketPlaceView')
    
    context = {
        'order_form':order_form,
        'cart_items':cart_items,
    }
    return render(request, 'orders/checkout.html', context)