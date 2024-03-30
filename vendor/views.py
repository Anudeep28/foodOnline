from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from accounts.decorators import check_restaurant_access
from accounts.forms import CustomUserForm, UserProfileForm
from accounts.models import User, UserProfile
from accounts.utils import send_verification_email
from menu.forms import CategoryModelForm, FoodItemModelForm
from menu.models import CategoryModel, FoodItemModel
from vendor.forms import VendorForm
from vendor.models import Vendor
# decorator
from django.contrib.auth.decorators import login_required, user_passes_test
# slugify
from django.template.defaultfilters import slugify

# Create your views here.

# helper function
def get_vendor(request):
    return Vendor.objects.get(user=request.user)

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
            vendor_name = vendor_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+"-"+ str(user.pk)
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            # After Saving the user the user should receive the
            # verification email to activate the account fromt he company
            mail_subject="Please activate your account"
            email_template_url='accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template_url)

            
            messages.success(request, "Your Restaurant has been registered ! Verification link is send on mail !")
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


# menu builder
@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def menuBuilder(request):
    vendor = get_vendor(request)
    categories = CategoryModel.objects.filter(vendor=vendor).order_by('created_at')
    context = {
        'categories':categories,
    }
    return render(request, 'vendor/restaurantMenuBuilder.html', context)

@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def menuBuilderCategory(request, pk=None):
    vendor = get_vendor(request)
    #category = CategoryModel.objects.get(pk=pk)
    category = get_object_or_404(CategoryModel,pk=pk)

    food_items = FoodItemModel.objects.filter(vendor=vendor, category=category)

    context = {
        'food_items':food_items,
        'category':category
    }
    return render(request, 'vendor/foodItem_by_category.html', context)


# Categoru CRUD
@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def addCategory(request):
    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST)
        if category_form.is_valid():
            category_name = category_form.cleaned_data['category_name']
            category = category_form.save(commit=False)
            category.vendor = get_vendor(request)
            
            category.save()
            #category_form.save()
            category.slug = slugify(category_name)+'-'+str(category.id)
            category.save()
            messages.success(request, "Category Added Successfully")
            return redirect('vendor:menuBuilder')
        else:
            messages.error(request, "Could not add the category!")
    else:
        category_form = CategoryModelForm()
    
    
    context = {
        'category_form':category_form
    }
    return render(request, 'vendor/addCategory.html', context)


@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def editCategory(request,pk=None):
    
    category_instance = get_object_or_404(CategoryModel,pk=pk)
    
    if request.method == 'POST':
        # The category instance should be passed into the 
        # form to recognise what it is editing
        category_form = CategoryModelForm(request.POST, instance=category_instance)
        if category_form.is_valid():
            category_name = category_form.cleaned_data['category_name']
            category = category_form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            category.save()
            #category_form.save()
            messages.success(request, "Category Updated Successfully")
            return redirect('vendor:menuBuilder')
        else:
            messages.error(request, "Could not Update the category!")
    else:
        category_form = CategoryModelForm(instance=category_instance)
    
    
    context = {
        'category_form':category_form,
        'category':category_instance
    }
    return render(request, 'vendor/editCategory.html', context)

@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def deleteCategory(request, pk=None):
    category_instance = get_object_or_404(CategoryModel, pk=pk)
    category_instance.delete()
    messages.success(request, "Category was deleted successfuly!")
    return redirect('vendor:menuBuilder')


@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def addFood(request):
    if request.method == 'POST':
        food_form = FoodItemModelForm(request.POST, request.FILES)
        if food_form.is_valid():
            food_title = food_form.cleaned_data['food_title']
            food = food_form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            food.save()
            #category_form.save()
            messages.success(request, "Food Item Added Successfully")
            return redirect('vendor:menuBuilderCategory',food.category.pk)
        else:
            messages.error(request, "Could not add the Food Item!")
    else:
        #category_form = CategoryModelForm()
        food_form = FoodItemModelForm()
        # modify the form so that it only print the 
        # categories of the logged in vendor
        food_form.fields['category'].queryset = CategoryModel.objects.filter(vendor=get_vendor(request))
    context = {
        'food_form':food_form,
    }
    return render(request, 'vendor/food/addFood.html', context)


@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def editFood(request, pk=None):
    food_instance = get_object_or_404(FoodItemModel,pk=pk)
    
    if request.method == 'POST':
        # The category instance should be passed into the 
        # form to recognise what it is editing
        food_form = FoodItemModelForm(request.POST, request.FILES,  instance=food_instance)
        if food_form.is_valid():
            food_title = food_form.cleaned_data['food_title']
            food = food_form.save(commit=False)
            food.vendor = get_vendor(request)
            food.slug = slugify(food_title)
            food.save()
            #category_form.save()
            messages.success(request, "Food Item Updated Successfully")
            return redirect('vendor:menuBuilderCategory',food.category.pk)
        else:
            messages.error(request, "Could not Update the Food Item!")
    else:
        food_form = FoodItemModelForm(instance=food_instance)
        food_form.fields['category'].queryset = CategoryModel.objects.filter(vendor=get_vendor(request))
    
    context = {
        'food_form':food_form,
        'food':food_instance
    }
    return render(request, 'vendor/food/editFood.html', context)

@login_required(login_url='accounts:userLogin')
@user_passes_test(check_restaurant_access)
def deleteFood(request, pk=None):
    food_instance = get_object_or_404(FoodItemModel,pk=pk)
    food_instance.delete()
    messages.success(request, "Food Item was deleted successfuly!")
    return redirect('vendor:menuBuilderCategory',food_instance.category.pk)