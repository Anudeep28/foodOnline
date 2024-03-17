from django.conf import settings
from vendor.models import Vendor


def get_restaurant(request):
    try:
        restaurant = Vendor.objects.get(user=request.user)
    except:
        restaurant = None
    return dict(restaurant=restaurant)


# In the template the key is not accessible
# hence we need it to be available in all templates
def get_google_api_key(request):
    return {'GOOGLE_API_KEY':settings.GOOGLE_API_KEY}