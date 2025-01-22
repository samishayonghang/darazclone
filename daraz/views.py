from django.shortcuts import render
from.forms import UserForm,LoginForm

# Create your views here.
def register(request):
    form=UserForm()
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
         form.save()
    else:
     print(form.errors)

    return render(request,'daraz/register.html',{'form':form})

def home(request):
    return render(request,'daraz/base.html')


def loginpage(request):
   form=LoginForm()
   if request.method=="POST" :
      form=LoginForm(request.POST)
      if form.is_valid():
         form.save()


   return render(request,'daraz/login.html',{'form':form})

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