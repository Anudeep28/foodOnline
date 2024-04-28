from django.shortcuts import get_object_or_404, redirect, render
# decorator
from django.contrib.auth.decorators import login_required
# Messages seervice
from django.contrib import messages

from accounts.forms import UserInfoForm, UserProfileForm
from accounts.models import UserProfile

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