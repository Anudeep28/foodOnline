from datetime import date, datetime, time
from enum import unique
from urllib import request
from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)

    user_profile = models.OneToOneField(UserProfile, related_name="userprofile", on_delete=models.CASCADE)

    vendor_name = models.CharField(max_length=20)

    vendor_slug = models.SlugField(max_length=100, unique=True)

    vendor_lincense = models.ImageField(upload_to='vendor/license')

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    
    # In order the vedore or restaurant to show Dynamic
    # open and close values for the restaurant to get updated
    # based ont hhe current time we are going to create our method
    # inside the class of vendor model
    def is_open(self):
        # Check current day openign hours
        todays_date = date.today()
        # returns weeek no
        today = todays_date.isoweekday()
        current_opening_hours = openingHoursModel.objects.filter(vendor=self, day = today)
        # check for current time
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        is_open = None
        for i in current_opening_hours:
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hours, "%I:%M %p").time())
                end = str(datetime.strptime(i.to_hours, "%I:%M %p").time())
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open =False
        return is_open
    
    # Now adding a functionality that when the admin
    # approves the restaurant the the restaurant receives
    # the nootification of approval
    # to access admin save button this is the way
    def save(self, *args, **kwargs):
        if self.pk is not None:
            # update
            original_val = Vendor.objects.get(pk=self.pk)
            
            if original_val.is_approved != self.is_approved:
                email_template_url = "vendor/emails/admin_notification_email.html"
                context = {
                    'user':self.user,
                    'is_approved':self.is_approved
                }
                if self.is_approved:
                    # send email notification
                    mail_subject = "Congratulations! Your Restaurant is now Approved"
                    
                    send_notification(mail_subject, email_template_url, context)
                else:
                    # send email
                    mail_subject = "We are Sorry! Your are not eligible for publishing on our website "
                    
                    send_notification(mail_subject, email_template_url, context)
        return super(Vendor,self).save(*args, **kwargs)
    

DAYS = [
    (1, ('Monday')),
    (2, ('Tuesday')),
    (3, ('Wednesday')),
    (4, ('Thursday')),
    (5, ('Friday')),
    (6, ('Saturday')),
    (7, ('Sunday')),
]

HOUR_OF_DAY = [(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range(0,24) for m in (0,30)]

# Opening hours of the restaurant
class openingHoursModel(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hours = models.CharField(choices=HOUR_OF_DAY,max_length=10, blank=True)
    to_hours = models.CharField(choices=HOUR_OF_DAY, max_length=10, blank=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        ordering = ('day','-from_hours')
        unique_together = ('vendor','day','from_hours','to_hours')

    def __str__(self) -> str:
        # to display the days instead of integers
        # we use get_fieldName_display() to display choices
        return self.get_day_display()