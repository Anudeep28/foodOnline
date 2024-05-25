from django.http import HttpResponse, JsonResponse
import simplejson as json
from django.shortcuts import redirect, render

from accounts.models import UserProfile
from accounts.utils import send_notification
from marketplace.context_processors import get_cart_amount
from marketplace.models import cartModel, taxModel
from menu.models import FoodItemModel
from orders.forms import OrderModelForm
# decorators
from django.contrib.auth.decorators import login_required

from orders.models import OrderModel, OrderedFoodModel, PaymentModel
from orders.utils import generate_order_number

# for razorpay setting
from mainSite.settings import RZP_KEY_ID, RZP_KEY_SECRET

# RazopPay
import razorpay

import vendor

# Creating request
client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))

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

# Create your views here.
@login_required(login_url='accounts:userLogin')
def placeOrderView(request):
    # cart model
    cart_items = cartModel.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace:marketPlaceView')
    
    # extract restaurants unique ID
    restaurant_id = []
    for i in cart_items:
        if i.food_item.vendor.pk not in restaurant_id:
            restaurant_id.append(i.food_item.vendor.pk)

    # to get the individual fooditem and vendor total
    get_tax = taxModel.objects.filter(is_active=True)
    subtotal = 0
    k = {}
    total_data = {}
    for i in cart_items:
        fooditem = FoodItemModel.objects.get(pk=i.food_item.pk, vendor_id__in=restaurant_id)
        r_id = fooditem.vendor.pk
        if r_id in k:
            subtotal = k[r_id]
            subtotal += (fooditem.price * i.quantity)
            k[r_id] = subtotal
        else:
            subtotal = (fooditem.price * i.quantity)
            k[r_id] = subtotal
        
        # Calculatae tax dict
        tax_dict = {}
        for i in get_tax:
            tax_type = i.tax_type
            tax_perc = i.tax_percentage
            tax_amount = round((tax_perc * subtotal)/100,2)
            tax_dict[tax_type] = {str(tax_perc):tax_amount}
        # Construct total data
        total_data.update({fooditem.vendor.pk:{str(subtotal):str(tax_dict)}})

    # Calculate the tax data

    #print(restaurant_id)
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
            order.total_data = json.dumps(total_data)
            order.total_tax = total_tax # type: ignore
            order.payment_method = request.POST['payment_method']
            #order.order_number = generate_order_number(order.pk)
            order.save()
            order.order_number = generate_order_number(order.pk)
            order.vendors.add(*restaurant_id)
            order.save()

            # RAZORPAY PAYMENT GATEWAY
            data = { "amount": float(order.total)*100,
                     "currency": "INR",
                       "receipt": "receipt_"+order.order_number }
            rzp_order = client.order.create(data=data)
            rzp_order_id = rzp_order['id']
            #print(rzp_order)
            context = {
                'order':order,
                'cart_items':cart_items,
                'rzp_order_id':rzp_order_id,
                'RZP_KEY_ID':RZP_KEY_ID,
                'rzp_amount':float(order.total)*100,
            }
            return render(request,'orders/placeOrder.html', context)#redirect('orders:placeOrder')
        else:
            print(order_form.errors)
    
    return render(request,'orders/placeOrder.html')

# Create your views here.
@login_required(login_url='accounts:userLogin')
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

            


            # Send order confirmation email to the customer
            mail_subject = "Thank you for ordering with us."
            email_template_url = 'orders/order_confirmation_mail.html'
            context = {
                'user': request.user,
                'order':order,
                'to_email':order.email
            }
            send_notification(mail_subject=mail_subject, email_template_url=email_template_url, context=context)
            #return HttpResponse("Saved Ordered Food")
            # order received email to the vendor
            mail_subject = "You have received a new Order"
            email_template_url = 'orders/new_order_received_mail.html'
            to_emails = []
            for i in cart_items:
                if i.food_item.vendor.user.email not in to_emails:
                    to_emails.append(i.food_item.vendor.user.email)
            context = {
                #'user': request.user,
                'order':order,
                'to_email':to_emails
            }
            send_notification(mail_subject=mail_subject, email_template_url=email_template_url, context=context)
            

            # Delete the cart items now
            # cart_items.delete()
            

            # return back to ajax with success or fail
            response = {
                'order_number':order_number,
                'transaction_id': transaction_id,
                #'payment_method' : payment_method,
                #'amount' : order.total,
            }
            return JsonResponse(response)
    return HttpResponse('Payments View')

def orderCompletedView(request):
    order_number = request.GET.get('order_no')
    transaction_id = request.GET.get('trans_id')
    try:
        order = OrderModel.objects.get(order_number = order_number, payment__transaction_id = transaction_id, is_ordered = True)
        ordered_food = OrderedFoodModel.objects.filter(order = order)

        subtotal = 0
        for item in ordered_food:
            subtotal += (item.price*item.quantity)
        tax_data = json.loads(order.tax_data)
        context = {
            'order':order,
            'ordered_food':ordered_food,
            'subtotal':subtotal,
            'tax_data':tax_data,
        }
        return render(request, 'orders/order_completed.html', context)
    except:
        return redirect('home')