"""
URL configuration for mainSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    #App
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('vendor/', include('vendor.urls', namespace='vendor')),
    path('marketplace/', include('marketplace.urls', namespace='marketplace')),
    path('customers/', include('customers.urls', namespace='customers')),
    path('orders/', include('orders.urls', namespace='orders')),
    

    # Home page of the app
    path('', views.HomePageView, name='home'),

    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
