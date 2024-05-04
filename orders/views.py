from django.http import HttpResponse
import simplejson as json
from django.shortcuts import redirect, render

from accounts.models import UserProfile
from marketplace.context_processors import get_cart_amount
from marketplace.models import cartModel
from orders.forms import OrderModelForm
# decorators
from django.contrib.auth.decorators import login_required

from orders.models import OrderModel, OrderedFoodModel, PaymentModel
from orders.utils import generate_order_number

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


def placeOrderView(request):
    # cart model
    cart_items = cartModel.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace:marketPlaceView')
    # now get the subtotal using the context_processor function
    subtotal = get_cart_amount(request)['subtotal']
    total_tax = get_cart_amount(request)['tax']
    grand_total = get_cart_amount(request)['grand_total']
    tax_data = get_cart_amount(request)['tax_dict']

    # checking if request is post
    # we gave action in the form to be directed to this view
    # on clicng the button
    if request.method == 'POST':
        # now getting the order form here 
        order_form = OrderModelForm(request.POST)
        if order_form.is_valid():
            # initialize the order model blank slate
            # newly creating the model for the user
            order = OrderModel()
            order.first_name = order_form.cleaned_data['first_name']
            order.last_name = order_form.cleaned_data['last_name']
            order.phone = order_form.cleaned_data['phone']
            order.email = order_form.cleaned_data['email']
            order.address = order_form.cleaned_data['address']
            order.country = order_form.cleaned_data['country']
            order.state = order_form.cleaned_data['state']
            order.city = order_form.cleaned_data['city']
            order.pin_code = order_form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total # type: ignore
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax # type: ignore
            order.payment_method = request.POST['payment_method']
            #order.order_number = generate_order_number(order.pk)
            order.save()
            order.order_number = generate_order_number(order.pk)
            order.save()
            context = {
                'order':order,
                'cart_items':cart_items
            }
            return render(request,'orders/placeOrder.html', context)#redirect('orders:placeOrder')
        else:
            print(order_form.errors)
    
    return render(request,'orders/placeOrder.html')

def paymentsView(request):
    # Check if the request is ajax or not
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method=='POST':
            # store the payment details
            order_number = request.POST.get('order_number')
            transaction_id = request.POST.get('transaction_id')
            payment_method = request.POST.get('payment_method')
            status = request.POST.get('status')
            # take the order instance now
            order = OrderModel.objects.get(user=request.user, order_number=order_number)
            payment = PaymentModel(
                user = request.user,
                transaction_id = transaction_id,
                payment_method = payment_method,
                amount = order.total,
                status = status
            )
            payment.save()
        
            # Update the order model
            order.payment = payment
            order.is_ordered = True
            order.save()
            # move the cart items to ordered food model
            cart_items = cartModel.objects.filter(user=request.user)
            for item in cart_items:
                ordered_food = OrderedFoodModel()
                ordered_food.order = order
                ordered_food.payment = payment
                ordered_food.user = request.user
                ordered_food.fooditem = item.food_item
                ordered_food.quantity = item.quantity
                ordered_food.price = item.food_item.price # type: ignore
                ordered_food.amount = item.food_item.price * item.quantity # type: ignore
                ordered_food.save()

            return HttpResponse("Saved Ordered Food")


            # Send order confirmation email to the customer
            # order received email to the vendor
            # return back to ajax with success or fail
    return HttpResponse('Payments View')