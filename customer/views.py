from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.
def customerdashboard(request):
    return render(request,'customer/customer.html')
def changepass(request):
    if request.method=="POST":
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            logout(request)
            messages.success(request,'password changed sucessfully')
            redirect('login')
        else:
            for field,errors in form.errors.items():
                for error in errors:
                    messages.error(request,error)

        
     
        
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'customer/changepass.html')