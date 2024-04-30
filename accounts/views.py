from django.shortcuts import render, redirect

from accounts.decorators import check_customer_access, check_restaurant_access
from accounts.utils import detectUser, send_verification_email
from vendor.models import Vendor
from .forms import CustomUserForm
from .models import User
# Messages
from django.contrib import messages, auth
# decorator
from django.contrib.auth.decorators import login_required, user_passes_test
# uid decoder
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator





# Create your views here.

def userRegisterView(request):
    # To check wether the user is logged in
    # to avoid again logging in by the user
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in !")
        return redirect('accounts:accountDecider')
    
    #form = CustomUserForm()
    # to check if it is post or not
    elif request.method == "POST":
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
            user = User.objects.create_user(first_name=first_name, # type: ignore
                                            last_name=last_name,
                                            username = username,
                                            email=email,
                                            password=password)
            user.role = User.CUSTOMER
            user.phone_number = phone_number
            user.save()
            
            # After Saving the user the user should receive the
            # verification email to activate the account fromt he company
            mail_subject="Please activate your account"
            email_template_url='accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template_url)

            # Messages
            messages.success(request, "You have been successfully Registered! Verification mail have been sent to your email id")
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
    return render(request, 'vendor/restaurantDashboard.html')



def activate(request, uidb64, token):
    # Activate the user by setting the user.is_active to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations, your account is active now")
        return redirect('accounts:accountDecider')
    else:
        messages.error(request, "Invalid activation link!")
        return redirect('accounts:accountDecider')
    


def forgot_password(request):
    # if post
    if request.method == 'POST':
        email = request.POST['email']

        # check if the user exists
        if User.objects.filter(email=email).exists():
            # exact is to get the exact same email address typed by the user
            user = User.objects.get(email__exact=email)
            # after gettign the user send the exact password reset email
            mail_subject="Reset your Password"
            email_template_url='accounts/passwords/password_reset_email.html'
            send_verification_email(request, user, mail_subject, email_template_url)

            messages.success(request, "Password reset link has been sent successfully!")

            return redirect('accounts:userLogin')
        else:
            messages.success(request, "Account does not exist!")

            return redirect('accounts:forgot_password')
        

    return render(request, 'accounts/passwords/forgot_password.html')



def reset_password_validate(request, uidb64, token):
    # Validate the user token and id
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, "Please reset the password")
        return redirect('accounts:reset_password')
    else:
        messages.error(request, "This link has been expired!")
        return redirect('accounts:accountDecider')

def reset_password(request):
    # reset the password
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
    
        if password == confirm_password:
            # get the user
            # recover the uid from the request session w e saved earlier
            user = User.objects.get(pk=request.session.get('uid'))
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password have been successfully changed!")
            return redirect('accounts:userLogin')
        else:
            messages.error(request, "Passwords did not match")
            return redirect('accounts:reset_password')

    return render(request, 'accounts/passwords/reset_password.html')