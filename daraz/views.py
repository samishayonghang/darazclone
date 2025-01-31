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
from django.http import JsonResponse,HttpResponse
from daraz.utils import send_activation_email,send_resetpassword_email
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
   
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
     if request.user.is_authenticated:  # Check if user is logged in
        name = request.user.name  
        # Get the name field (custom user model)
     else:
        name = None  # No u
     return render(request,'daraz/base.html',{'name':name})


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

def addtocart(request):
   if request.method=="POST":
      user=request.user
      product_id=request.POST.get('prod_id')
      product=Product.objects.get(id=product_id)

      Cart.objects.create(user=user,product=product).save()
      return redirect('cart')
      

      


def showcart(request):
   if request.user.is_authenticated:
      user=request.user
      cart=Cart.objects.filter(user=user)
      print(cart)
      amount=0.0
      shippingamount=100.0
      totalamount=0.0
      cart_product=[p for p in Cart.objects.all()if p.user==user]
      #print(cart_product)
      if cart_product:
         for p in cart_product:
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
         totalamount=amount+shippingamount

   return render(request,'daraz/cart.html',{'carts':cart,'totalamount':totalamount,'amount':amount,'shippingamount':shippingamount})
@login_required
def plus_cart(request):
    if request.method == "GET":
        user = request.user
        prod_id = request.GET.get('prod_id')

        # Get the user's cart for the specific product
        carts = Cart.objects.filter(product_id=int(prod_id), user=user)

        if carts.exists():
            cart = carts.first()
            cart.quantity += 1
            cart.save()

            # Calculate the updated amount and total amount
            amount = 0.0
            shippingamount = 100.0  # Static shipping cost (adjust as needed)

            # Calculate total amount for all cart items
            cart_products = Cart.objects.filter(user=user)
            for p in cart_products:
                amount += p.quantity * p.product.discounted_price

            # Calculate total amount including shipping
            totalamount = amount + shippingamount

            # Prepare the response data
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': totalamount,
                'shippingamount': shippingamount
            }

            return JsonResponse(data)
        
def minus_cart(request):
   if request.method=="GET":
      user=request.user
      prod_id=request.GET.get('prod_id')
      carts=Cart.objects.filter(product_id=int(prod_id),user=user)
      if carts.exists():
         cart=carts.first()
         if cart.quantity > 1:
  
          cart.quantity -= 1
          cart.save()
         else:
          cart.delete()  # 
         amount = 0.0
         shippingamount = 100.0  # Static shipping cost (adjust as needed)

            # Calculate total amount for all cart items
         cart_products = Cart.objects.filter(user=user)
         for p in cart_products:
            amount += p.quantity * p.product.discounted_price

            # Calculate total amount including shipping
         totalamount = amount + shippingamount

            # Prepare the response data
         data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': totalamount,
                'shippingamount': shippingamount
            }

         return JsonResponse(data)
def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        
        if not prod_id:
            return HttpResponse("Product ID is required", status=400)
        
        try:
            prod_id = int(prod_id)  # Convert prod_id to an integer
        except ValueError:
            return HttpResponse("Invalid Product ID", status=400)
        
        user = request.user  # Assuming the user is logged in
        
        # Filter the cart using the valid prod_id
        carts = Cart.objects.filter(product_id=prod_id, user=user)

        if not carts.exists():
            return HttpResponse("No cart items found for this product.", status=404)
        
        # Remove the cart items
        carts.delete()

        amount = 0.0
        shippingamount = 100.0  # Static shipping cost (adjust as needed)

        # Calculate total amount for remaining cart items
        cart_products = Cart.objects.filter(user=user)
        for p in cart_products:
            amount += p.quantity * p.product.discounted_price

        # Calculate total amount including shipping
        totalamount = amount + shippingamount

        # Prepare the response data
        data = {
            'amount': amount,
            'totalamount': totalamount,
            'shippingamount': shippingamount
        }

        return JsonResponse(data)

    return HttpResponse("Invalid request method")

    # If the request method is not GET
    
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


def profile(request):
   province_choices = Customer._meta.get_field('province').choices
   city_choices=Customer._meta.get_field('city').choices
   gender_choices=Customer._meta.get_field('gender').choices
  
   if request.method=="POST":
      usr=request.user
      name=request.POST.get('name')
      phone_number=request.POST.get('phone_number')
      province=request.POST.get('province')
      city=request.POST.get('city')
      landmark=request.POST.get('landmark')
      gender=request.POST.get('gender')
      Customer.objects.create(user=usr,
                            name=name,
                           phone_number=phone_number,
                           province=province,
                           city=city,
                           landmark=landmark,
                           gender=gender,
                        )
   
      messages.success(request,"your profile updated sucessfully")
      return redirect('manageacc')
      
   

   return render(request,'daraz/profile.html',{'province_choices':province_choices,'city_choices':city_choices,'gender_choices':gender_choices})


def manageacc(request):
   
      try:
        profile=Customer.objects.get(user=request.user)
      except Customer.DoesNotExist:
         profile=None
      except Customer.MultipleObjectsReturned:
        # Handle the case where multiple records exist for the same user
        profile = Customer.objects.filter(user=request.user).first()  # Or handle accordingly

      return render(request,'daraz/manageacc.html',{'profile':profile})
def checkout(request):
   
   
   customer=Customer.objects.filter(user=request.user).first()
  
   cart_items=Cart.objects.filter(user=request.user)
   amount = 0.0
   shippingamount = 100.0  # Static shipping cost (adjust as needed)

            # Calculate total amount for all cart items
   cart_products = Cart.objects.filter(user=request.user)
   if cart_products:
    for p in cart_products:
       
       amount += p.quantity * p.product.discounted_price


     
          # Calculate total amount including shipping
    totalamount = amount + shippingamount



   

   
   

   return render(request,'daraz/checkout.html',{'customer':customer,'cart':cart_items,'totalamount':totalamount,'shippingamount':shippingamount,'amount':amount})