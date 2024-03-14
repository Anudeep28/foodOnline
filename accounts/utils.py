# Redirect URL decider

def detectUser(user):
    if user.get_role() == 'restaurant':
        redirecturl =  "accounts:restaurantDashboard"
    elif user.get_role() == 'customer':
        redirecturl = "accounts:customerDashboard"
    elif user.role == None and user.is_superadmin:
        redirecturl = "/admin"
    return redirecturl