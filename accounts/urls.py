from django.urls import path
from . import views

app_name='accounts'

urlpatterns = [
    #App
    path('userRegister/', views.userRegister , name='userRegister'),

]