from django.shortcuts import render,redirect,get_object_or_404
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
import hmac
import hashlib
import base64
import uuid
import requests

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
     product=Product.objects.all()
 
     if request.user.is_authenticated:
         
         name = request.user.name  
        # Get the name field (custom user model)
     else:
        name = None  # No u
     return render(request,'daraz/base.html',{'name':name,'products':product})


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
def remove_cart(request,prod_id):
    if request.method == "GET":
       
        print(f"Received prod_id: {prod_id}") 
        
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
        return redirect('cart')

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
  
   
   amount = 0.0
   shippingamount = 100.0  # Static shipping cost (adjust as needed)

            # Calculate total amount for all cart items
   cart_products = Cart.objects.filter(user=request.user)
   if cart_products:
    for p in cart_products:
       
       p.amount = p.quantity * p.product.discounted_price
       amount += p.amount


     
          # Calculate total amount including shipping
   totalamount = amount + shippingamount
   return render(request,'daraz/checkout.html',{'customer':customer,'cart_products':cart_products,'totalamount':totalamount,'shippingamount':shippingamount,'amount':amount})

def gotoesewa(request):
   return render(request,'daraz/gotoesewa.html')  



def generate_signature(totalamount, transaction_uuid, product_code, secret_key):
    data = f"{totalamount}|{transaction_uuid}|{product_code}|{secret_key}"
    signature = hashlib.sha256(data.encode('utf-8')).hexdigest()
    return signature
    

def payment_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    print(f"Cart Items: {cart_items}")
    
    
    # Calculate the amount
    amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
    product_code = [item.product.id for item in cart_items]
    print(product_code)
    product_delivery_charge = 100.0  # You can replace this with dynamic delivery charge if needed
    total_amount = float(amount) + product_delivery_charge
    
    # Generate the transaction UUID
    transaction_uuid = str(uuid.uuid4())

    # Fetch the selected product based on the product_id passed via GET
   
    
    

    # Secret key for signature
    secret_key = "8gBm/:&EnhH.1/q"  # Replace with your secret key
    signed_field_names = "total_amount,transaction_uuid,product_code,secret_key"


    # Generate the signature
    signature = generate_signature(str(total_amount), transaction_uuid, product_code, secret_key)
    print(f"Generated Signature: {signature}")  
    print(f"Amount: {amount}")
    print(f"Total Amount: {total_amount}")
    print(f"Transaction UUID: {transaction_uuid}")
    print(f"Product Code: {product_code}")
    

    # Prepare the data to pass to the template
    url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
    data = {
        "amount": str(amount),
        "tax_amount": "0",
        "total_amount": str(total_amount),
        "transaction_uuid": transaction_uuid,
        "product_code": product_code,
        "product_service_charge": "0",
        "product_delivery_charge": str(product_delivery_charge),
        "success_url": "http://127.0.0.1:8000/payment/success/",
        "failure_url": "http://127.0.0.1:8000/payment/failure/",
        "signed_field_names": signed_field_names,
        "signature": signature
    }
    response = requests.post(url, data=data)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")

# If the response is JSON, print the parsed response
    try:
     response_json = response.json()
     print(f"JSON Response: {response_json}")
    except ValueError:
     print("Response is not in JSON format.")
    
    # Render the payment page with the data
    return render(request, 'daraz/esewarequest.html', {"cart_items": cart_items, **data})

def payment_success(request):
    ref_id = request.GET.get('refId')
    verification_url = "https://uat.esewa.com.np/epay/transrec"

    data = {
        'amt': request.GET.get('amt'),
        'scd': 'EPAYTEST',
        'pid': request.GET.get('pid'),
        'rid': ref_id
    }

    # Make the verification request to eSewa's server
    response = request.post(verification_url, data=data)
    
    if 'Success' in response.text:
        Cart.objects.filter(user=request.user).delete()  # Clear the cart after successful payment
        return HttpResponse("Payment Successful and Verified!")
    else:
        return HttpResponse("Payment Verification Failed!")

def payment_failure(request):
    return HttpResponse("Payment Failed! Please try again.")


def paymentdone(request):
   if request.method=="POST":
    user=request.user
    custid=request.POST.get('custid')
    customer=get_object_or_404(Customer,id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
      Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()

      
    
   return render(request,'daraz/payment.html')
   
      

  

def order(request):
   print(f"Logged-in user: {request.user}")
   od=Orderplaced.objects.filter(user=request.user)
   print(od)
   for order in od:
        print(f"Order ID: {order.id}, Product: {order.product}, Discounted Price: {order.product.discounted_price}, Quantity: {order.quantity}")
        
   if not od.exists():
        return render(request, 'daraz/order.html', {'orderplace': od, 'message': 'No orders found.'})
   amount = 0.0
   shippingamount= 100.00

    # Loop through the orders to calculate the total amount for each order
   for order in od:
        # Calculate total price for each order (product price * quantity)
        order.amount = order.product.discounted_price * order.quantity
        amount += order.amount
        
   totalamount=amount + shippingamount
   return render(request,'daraz/order.html',{'od':od,'totalamount':totalamount,'shippingamount':shippingamount,'amount':amount})


def buynow(request,prod_id):
   
   
   customer=Customer.objects.filter(user=request.user).first()
  
   
   amount = 0.0
   shippingamount = 100.0  # Static shipping cost (adjust as needed)

            # Calculate total amount for all cart items
   products = Product.objects.filter(id=prod_id).first()
   
   
   quantity=1
       
   products.amount = quantity * products.discounted_price
   amount += products.amount


     
          # Calculate total amount including shipping
   totalamount = amount + shippingamount
   return render(request,'daraz/buy.html',{'customer':customer,'products':products,'totalamount':totalamount,'shippingamount':shippingamount,'amount':amount})

