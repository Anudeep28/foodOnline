from django.shortcuts import render, redirect
from .forms import CustomUserForm
from .models import User
# Messages
from django.contrib import messages
# Create your views here.

def userRegisterView(request):
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


