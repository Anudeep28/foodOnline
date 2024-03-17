from django.core.exceptions import PermissionDenied

# creating a custom decorator to restrict the user
def check_customer_access(user):
    if user.get_role() == 'customer':
        return True
    else:
        raise PermissionDenied
    

def check_restaurant_access(user):    
    if user.get_role() == 'restaurant':
        return True
    else:
        raise PermissionDenied