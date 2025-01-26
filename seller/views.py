from django.shortcuts import render

# Create your views here.
def sellerdashboard(request):
    return render(request,'seller/sellerdashboard.html')
def changepass(request):
    return render(request,'seller/changepassword.html')