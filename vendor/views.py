from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.decorators import check_restaurant_access
from accounts.forms import CustomUserForm, UserProfileForm
from accounts.models import User, UserProfile
from accounts.utils import send_verification_email
from vendor.forms import VendorForm
from vendor.models import Vendor
# decorator
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.


def vendorRegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect('accounts:accountDecider')

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
            # After Saving the user the user should receive the
            # verification email to activate the account fromt he company
            mail_subject="Please activate your account"
            email_template_url='accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template_url)

            
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

@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def restaurantProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)

    # if the user updates the information
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        restaurant_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and restaurant_form.is_valid():
            profile_form.save()
            restaurant_form.save()
            messages.success(request, "Updated successfully!")
            return redirect('vendor:restaurantProfile')
        else:
            messages.error(request, "Found Some errors")
    else:
        profile_form = UserProfileForm(instance=profile)
        restaurant_form = VendorForm(instance=vendor)

    context = {
        "profile_form":profile_form,
        "restaurant_form":restaurant_form,
        "profile":profile,
        "vendor":vendor
    }
    return render(request, 'vendor/restaurantProfile.html', context)