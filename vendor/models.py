from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification
# Create your models here.


class Vendor(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)

    user_profile = models.OneToOneField(UserProfile, related_name="userprofile", on_delete=models.CASCADE)

    vendor_name = models.CharField(max_length=20)

    vendor_lincense = models.ImageField(upload_to='vendor/license')

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name
    
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