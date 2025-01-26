from django.contrib import admin
from daraz.models import User,Customer,Product,Cart,Orderplaced
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserModelAdmin(UserAdmin):
    model=User
    list_display=["id","email","name","is_active","is_staff","is_seller","is_customer","is_superuser"]
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

@admin.register(Customer) 
class CustomerModelAdmin(admin.ModelAdmin):
    list_display=['user','name','province','city','address','landmark','phone_number']



@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
     list_display = ('id', 'title', 'selling_price', 'discounted_price', 'brand', 'category', 'product_image')


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
      list_display = ('id', 'user', 'product', 'quantity')

@admin.register(Orderplaced)
class OrderplacedAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status')