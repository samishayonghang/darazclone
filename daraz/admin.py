from django.contrib import admin
from daraz.models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModelAdmin(UserAdmin):
    model=User
    list_display=["id","email","name","city","is_active","is_staff","is_seller","is_customer","is_superuser"]
    list_filter=["is_superuser"]
    fieldsets =[
        ("User credentials", {"fields":["email","password"]}),
        ("personal Information",{"fields":["name","city"]}),
        ("permissions",{"fields":["is_active","is_staff" ,"is_seller","is_superuser",]}),


    ]
    search_fields=["email"]
    ordering=["email","id"]
    filter_horizontal=[]
admin.site.register(User,UserModelAdmin)
    
