from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# this import is for Location field
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
# Create your models here.

# BASEUSERMANAGER allow sto Edit how the users are created 

class UserManager(BaseUserManager):
    
    # Method 
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email or not username:
            raise ValueError('User must provide Email address and username')
        
        user = self.model(
            # normalize will normalize the email address to lowercase
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,

        )

        # set password will encode the password
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # Now for superuser
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            username = username,
            password=password,
        )
        user.is_admin =True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Instead of AbstractUSEr model we use AbstractBaseUserModel whihc gives 
# full contro of the Django user model
class User(AbstractBaseUser):
    # Choices defining
    RESTAURANT = 1
    CUSTOMER = 2

    ROLE = (
        (RESTAURANT,'Restaurant'),
        (CUSTOMER,'Customer'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE, blank=True, null = True)

    # Required fileds are 
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date =models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # to overqrite username login field to email login field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    # internal function inside models
    # to determine wether the use is vendor 
    # or customer
    def get_role(self):
        if self.role == 1:
            user_role = 'restaurant'
        elif self.role == 2:
            user_role = 'customer'
        return user_role 


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    cover_photo = models.ImageField(upload_to='users/cover_pictures', blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    location = gismodels.PointField(blank=True, null=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.first_name
    

    # Overwriting save method
    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            # creating point from long and lat
            self.location = Point(float(self.longitude), float(self.latitude))
            return super(UserProfile, self).save(*args, **kwargs)
        return super(UserProfile, self).save(*args, **kwargs)
        
    # to get the full adress\
    # def full_address(self):
    #     return self.address

        #profile.save()
# We also use the decorator to connect the post save and function
# as shown above
# post_save.connect(create_profile_user, sender=User)

