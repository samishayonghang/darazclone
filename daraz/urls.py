from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from.views import register,home,loginpage,saveapp,help,changelang,sellerregister,search,cart,flashsale,reset,changepassword,cart,buy,ProductView,activate,password_reset_confirm,logout_view,ProductDetailView
urlpatterns = [
   path('register/',register,name="register"),
   path('',home,name="home"),
   path('login/',loginpage,name='login'),
   path('saveapp/',saveapp, name="saveapp"),
   path('sellerregister/',sellerregister, name="sellerregister"),
   path('help/',help, name='help'),
   path('changelang/',changelang, name='changelang'),
   path('search/',search,name='search'),
   path('cart/',cart,name='cart'),
   path('flashsale/',flashsale,name='flashsale'),
   path('reset/',reset, name='resetpassword'),
   path('change/',changepassword, name='changepassword'),
   path('logout/',logout_view,name="logout"),
   
   path('buy/',buy,name='buy'),
   path('detail/<int:pk>',ProductDetailView.as_view(),name='detail'),
   path('insidecategory/',ProductView.as_view(),name='insidecategory'),
   path('activate/<str:uidb64>/<str:token>/',activate,name="activate"),
   path('password_reset_confirm/<uidb64>/<token>/',password_reset_confirm,name="password_reset_confirm")

   
   
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
