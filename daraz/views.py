from django.shortcuts import render,redirect
from.models import User,Customer,Product,Cart,Orderplaced
from django.views import View
from.forms import CustomUserCreationForm,PasswordResetForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from daraz.utils import send_activation_email,send_resetpassword_email
from django.contrib.auth.forms import SetPasswordForm
# Create your views here.
def register(request):
   print("smaisha")
   if request.method=="POST":
     form=CustomUserCreationForm(request.POST)
     if form.is_valid():
        user=form.save(commit=False)
        user.set_password(form.cleaned_data["password1"])
        user.is_active=False
        user.save()
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        token=default_token_generator.make_token(user)
        activation_link=reverse('activate',kwargs={'uidb64':uidb64,'token':token})
        activation_url = f"{settings.SITE_DOMAIN}{activation_link}"
        send_activation_email(user.email,activation_url)
        print(activation_url)




        messages.success(request,'Registration sucessfull please check your email to activate your account')
        return redirect('login')
     print(form.errors)
     
     

   else:
    form=CustomUserCreationForm()
     
   

   return render(request,'daraz/register.html',{'form':form})

def home(request):
    return render(request,'daraz/base.html')


def loginpage(request):
   if request.user.is_authenticated:
      if request.user.is_seller:
         return redirect('sellerdashboard')
      elif request.user.is_customer:
         return redirect('customerdashboard')
      return redirect('home')

   if request.method=="POST":
      print("POST request received")
      
      email=request.POST.get('email')
      password=request.POST.get('password')
      print(f"Email: {email}, Password: {password}")
      if not email or not password:
         messages.error(request,'Both field is required')
         return redirect('login')
      try:
         user=User.objects.get(email=email)
      except User.DoesNotExist:
         messages.error(request,'Invalid email or password')
         return redirect('login')

      if not user.is_active:
         messages.error(request,'please activate your account to login')
         return redirect('login')
      user=authenticate(request,email=email,password=password)
      if user is not None:
         login(request,user)
         if user.is_seller:
            return redirect('sellerdashboard')
         elif user.is_customer:
            return redirect('customerdashboard')
         else:
            messages.error(request,"you dont have permission to acess this area")
         return redirect('home')
      
      else:
         messages.error(request,"invalid email or password")
         return redirect('login')
      
   return render(request,'daraz/login.html')

def saveapp(request):
   return render(request,'daraz/saveapp.html')

def sellerregister(request):
   return render(request,'daraz/sellerregister.html')

def help(request):
   return render(request,'daraz/help.html')

def changelang(request):
   return render(request,'daraz/changelang.html')

def search(request):
   return render(request,'daraz/search.html')
def cart(request):
   return render(request,'daraz/cart.html')
def flashsale(request):
   return render(request,'daraz/flash.html')
def reset(request):
   if request.method=="POST":
      form=PasswordResetForm(request.POST)
      if form.is_valid():
         email=form.cleaned_data.get('email')
         user=User.objects.filter(email=email).first()
         if user:
           uidb64=urlsafe_base64_encode(force_bytes(user.pk))
           token=default_token_generator.make_token(user)
           reset_url=reverse('password_reset_confirm',kwargs={'uidb64':uidb64,'token':token})
           absolute_reset_url=f"{request.build_absolute_uri(reset_url)}"
           messages.success(request,"we have sent you a password reset link")
           send_resetpassword_email(user.email,absolute_reset_url)
           messages.success(request,"we have sent you a password resent link please check your email")
           return redirect('login')
           



   else:
      form=PasswordResetForm()
   return render(request,'daraz/reset.html',{'form':form})

def password_reset_confirm(request,uidb64,token):
   try:
      uid=force_str(urlsafe_base64_decode(uidb64))
      user=User.objects.get(pk=uid)
      if not default_token_generator.check_token(user,token):
         messages.error(request,'this link has expired or invalid')
         return redirect('resetpassword')
      if request.method=="POST":
         form=SetPasswordForm(user,request.POST)
         if form.is_valid():
            form.save()
            messages.success(request,'your password has been sucessfully reset')
            return redirect('login')
         else:
            for fields,errors in form.errors.items():
               for error in errors:
                  messages.error(request,error)
      else:
         form=SetPasswordForm(user)
      return render(request,'daraz/passwordconfirm_reset.html',{'form':form,'uidb64':uidb64,'token':token})
   
   except (TypeError,ValueError,OverflowError,User.DoesNotExist):
      messages.error(request,'an error occured please try agrain later')

def changepassword(request):
   return render(request,'daraz/changepassword.html')
def buy(request):
   return render(request,'daraz/buy.html')
#def detail(request):
   #return render(request,'daraz/detail.html')
class ProductDetailView(View):
   def get(self,request,pk):
      product= Product.objects.get(pk=pk)
      return render(request,'daraz/detail.html',{'product':product})


class ProductView(View):
   def get(self,request):
         category = request.GET.get('category', None)  # Default to None if not provided

        # Filter products based on the category
         if category == 'skincare':
            products = Product.objects.filter(category='skincare')
         elif category == 'groceries':
            products = Product.objects.filter(category='groceries')
         elif category == 'gadgets':
            products = Product.objects.filter(category='gadgets')
         elif category == 'winterchildren':
            products = Product.objects.filter(category='winterchildren')
         elif category == 'clothing':
            products = Product.objects.filter(category='clothing')
         else:
            products = None  # If no valid category, show nothing or handle it differently

        # Pass the filtered products to the template
         return render(request, 'daraz/insidecategory.html', {'products': products, 'category': category})
   



      
def activate(request,uidb64,token):
   try:
    uidb64=force_str(urlsafe_base64_decode(uidb64))
    user=User.objects.get(pk=uidb64)
    if user.is_active:
       messages.warning(request,"this account has already been activated")
       return redirect('login')
    
    if default_token_generator.check_token(user,token):
       user.is_active=True
       user.save()
       messages.success(request,"your account has been activated successfully")
       return redirect('login')
    else:
       messages.error(request,"the activation link is invalid or has expired")
       return redirect('login')
    


   except(TypeError,ValueError,OverflowError,User.DoesNotExist):
      messages.error(request,"invalid activation link")
      return redirect('login')
      
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully.")  # Logs out the user
        return redirect('login')  


