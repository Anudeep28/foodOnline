from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from mainSite import settings

# Redirect URL decider

def detectUser(user):
    if user.role == 1:
        redirecturl =  "accounts:restaurantDashboard"
    elif user.role == 2:
        redirecturl = "accounts:cusDashboard"
    elif user.role == None and user.is_superadmin:
        redirecturl = "/admin"
    return redirecturl


# Sending email function for registered user
def send_verification_email(request, user, mail_subject, email_template_url):
    
    # to get the current url site
    # this helps to divert based on the development
    # and deployment envirnment
    current_site = get_current_site(request)

    #mail_subject = "Please activate your account"
    message = render_to_string(email_template_url,
                               {
        'user':user,
        'domain':current_site,
        # encoded version of users primary key send to the ussr
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        # passing the token to the user ( generated token )
        'token': default_token_generator.make_token(user),
    })

    to_email = user.email
    mail = EmailMessage(mail_subject, 
                        message, 
                        from_email=settings.DEFAULT_FROM_EMAIL, 
                        to=[to_email])
    mail.send()


# Sending notification function
def send_notification(mail_subject, email_template_url, context):
    message = render_to_string(email_template_url, context)

    to_email = context['user'].email

    mail = EmailMessage(mail_subject, 
                        message, 
                        from_email=settings.DEFAULT_FROM_EMAIL, 
                        to=[to_email])
    mail.send()
# Sending email function for registered user
# def send_password_reset(request, user):
    
#     # to get the current url site
#     # this helps to divert based on the development
#     # and deployment envirnment
#     current_site = get_current_site(request)

#     mail_subject = "Reset your Password"
#     message = render_to_string('accounts/passwords/password_reset_email.html',{
#         'user':user,
#         'domain':current_site,
#         # encoded version of users primary key send to the ussr
#         'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#         # passing the token to the user ( generated token )
#         'token': default_token_generator.make_token(user),
#     })

#     to_email = user.email
#     mail = EmailMessage(mail_subject,message,from_email=settings.EMAIL_HOST_USER,to=[to_email])
#     mail.send()
