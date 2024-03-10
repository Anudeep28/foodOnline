from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.forms import CustomUserForm
from accounts.models import User, UserProfile
from vendor.forms import VendorForm

# Create your views here.
def vendorRegisterView(request):

    if request.method == 'POST':
        # store the Data and create the user and vendor
        form = CustomUserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)

        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            username = username,
                                            email=email,
                                            password=password)
            user.role = User.RESTAURANT
            user.phone_number = phone_number
            user.save()

            # Now the Vendor part
            vendor = vendor_form.save(commit=False)
            # now assign User and Userprofile to vendor model
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "Your Restaurant has been registered !!")
            return redirect('vendor:vendorRegister')
        else:
            messages.error(request, "Please check for the the errors !!")
    else:
        form = CustomUserForm()
        vendor_form = VendorForm()

    context = {
        "form":form,
        "vendor_form":vendor_form
    }
    return render(request, 'vendor/vendorRegister.html', context)