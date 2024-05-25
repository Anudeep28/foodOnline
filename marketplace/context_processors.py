from .models import cartModel, taxModel
from menu.models import FoodItemModel


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = cartModel.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity

            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amount(request):
    subtotal = 0
    tax = 0
    grand_total = 0
    tax_dict = {}
    if request.user.is_authenticated:
        cart_items = cartModel.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItemModel.objects.get(pk=item.food_item.pk)
            subtotal += (fooditem.price * item.quantity)

        get_tax = taxModel.objects.filter(is_active=True)
        for i in get_tax:
            tax_type = i.tax_type
            tax_perc = i.tax_percentage
            tax_amount = round((tax_perc * subtotal)/100,2)
            tax_dict[tax_type] = {str(tax_perc):str(tax_amount)}
            tax += tax_amount
        #print(tax)

        grand_total = subtotal + tax
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total, tax_dict=tax_dict)