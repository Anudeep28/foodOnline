from django.shortcuts import render, redirect

from accounts.decorators import check_customer_access, check_restaurant_access
from accounts.utils import detectUser
from .forms import CustomUserForm
from .models import User
# Messages
from django.contrib import messages, auth
# decorator
from django.contrib.auth.decorators import login_required, user_passes_test







# Create your views here.

def userRegisterView(request):
    # To check wether the user is logged in
    # to avoid again logging in by the user
    if request.user.is_authernticated:
        messages.warning(request, "You are already logged in !")
        return redirect('accounts:dashboard')
    
    #form = CustomUserForm()
    # to check if it is post or not
    if request.method == "POST":
        # request.POST has dictionary with field names and values
        form = CustomUserForm(request.POST)
        if form.is_valid():
            # # creating instance of the user
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # # Set the password to hasable
            # password = form.cleaned_data['password']
            # user.set_password(password)
            # # instead now of form we save the user
            # # which is the same functionality
            # user.save()
            # #form.save()

            # instead of above we can make use of the 
            # the baseUSermanager model we created
            # in the models.py file
            # as shown below
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
            user.role = User.CUSTOMER
            user.phone_number = phone_number
            user.save()

            # Messages
            messages.success(request, "You have been successfully Registered")
            return redirect('accounts:userRegister')
        else:
            #print("Invalid Form")
            #print(form.errors)
            messages.error(request, "Please check the errors !!")
    else:
        form = CustomUserForm()
    
    
    context = {
        "form":form
    }
    
    return render(request, 
                  'accounts/userRegister.html',
                  context)



def dashboard(request):
    return render(request, 'accounts/dashboard.html')



def userLogin(request):
    # To check wether the user is logged in
    # to avoid again logging in by the user
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect('accounts:accountDecider')
    
    # for post request
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('accounts:accountDecider')
        else:
            messages.error(request, "Invalid Login Credentials")
            return redirect('accounts:userLogin')

    return render(request, 'accounts/loginUser.html')


def userLogout(request):
    auth.logout(request)
    messages.info(request, "You have successfully Logged out !")
    return redirect('accounts:userLogin')


@login_required(login_url='accounts:userLogin')
def accountDecider(request):

    user = request.user

    redirecturl = detectUser(user)

    return redirect(redirecturl)


@login_required(login_url='accounts:userLogin')
@user_passes_test(check_customer_access)
def cusDashboard(request):
    return render(request, 'accounts/cusDashboard.html')


@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def restaurantDashboard(request):
    return render(request, 'accounts/restaurantDashboard.html')