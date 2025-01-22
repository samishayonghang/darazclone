from django.contrib import admin
from django.urls import path
from.views import register,home,loginpage,saveapp,help,changelang,sellerregister,search,cart
urlpatterns = [
   path('register/',register,name="register"),
   path('',home,name="home"),
   path('login/',loginpage,name='login'),
   path('saveapp/',saveapp, name="saveapp"),
   path('sellerregister/',sellerregister, name="sellerregister"),
   path('help/',help, name='help'),
   path('changelang/',changelang, name='changelang'),
   path('search/',search,name='search'),
   path('cart/',cart,name='cart')
   
   
   
   
]
