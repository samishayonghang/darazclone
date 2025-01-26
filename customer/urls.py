from django.contrib import admin
from django.urls import path,include
from.views import customerdashboard,changepass

urlpatterns = [
    path('customerdashboard/',customerdashboard,name="customerdashboard"),
    path('changepass/',changepass,name="changepass")
  
]