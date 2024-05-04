from django.conf import settings
from accounts.models import UserProfile
from vendor.models import Vendor


def get_restaurant(request):
    try:
        restaurant = Vendor.objects.get(user=request.user)
    except:
        restaurant = None
    return dict(restaurant=restaurant)

def get_customer_profile(request):
    try:
        customer_profile = UserProfile.objects.get(user=request.user)
    except:
        customer_profile = None
    return dict(customer_profile=customer_profile)


# In the template the key is not accessible
# hence we need it to be available in all templates
def get_google_api_key(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}

# In the template the key is not accessible
# hence we need it to be available in all templates
def get_paypal_api_key(request):
    return {'PAYPAL_CLIENT_ID':settings.PAYPAL_CLIENT_ID}