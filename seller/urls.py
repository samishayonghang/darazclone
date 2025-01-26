from django.contrib import admin
from django.urls import path,include
from.views import sellerdashboard,changepass

urlpatterns = [
    path('sellerdashboard/',sellerdashboard,name="sellerdashboard"),
    path('changepass/',changepass,name="changepass")
    
  
]