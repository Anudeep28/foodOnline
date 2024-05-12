from django.shortcuts import get_object_or_404, redirect, render
# decorator
from django.contrib.auth.decorators import login_required
# Messages seervice
from django.contrib import messages

from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import UserProfile
from orders.models import OrderModel, OrderedFoodModel

# Json
import simplejson as json

# Create your views here.
@login_required(login_url='accounts:userLogin')
def customerProfile(request):
    profile = get_object_or_404(UserProfile, user = request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance = profile)
        user_form = UserInfoForm(request.POST,instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, 'Profile Updated')
            return redirect('customers:profile')
        else:
            messages.error(request, "Errors in the profile form")
            print(profile_form.errors)
            print(user_form.errors)
    else:
        # initialize the forms for profile settings
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance = request.user)

    context = {
        'profile_form':profile_form,
        'user_form':user_form,
        'profile':profile,
    }
    return render(request, 'customers/customerProfile.html', context)


def myOrdersView(request):
    orders = OrderModel.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request, 'customers/cusMyOrders.html', context)

def OrderDetailsView(request,order_number):
    try:
        print('entered order')
        order = OrderModel.objects.get(order_number=order_number, is_ordered=True)
        ordered_food = OrderedFoodModel.objects.filter(order=order)
        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price * item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        
        return render(request, 'customers/OrderDetailsView.html', context)
    except:
        return redirect('accounts:cusDashboard')

    