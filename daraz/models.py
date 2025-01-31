from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None,):
        if not email:
            raise ValueError("User must have valid email address")
        user=self.model(email=self.normalize_email(email), name=name)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('superuser must have is_staff =True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('superuser must have is_superuser= True')

        user=self.create_user(email,password)
        user.is_staff=True
        user.is_superuser=True
        user.is_customer=True
        user.is_seller=True
        user.save(using=self._db)
        return user


CITY_FIELDS = (
    # Province No. 1
    ('Biratnagar', 'Biratnagar'),
    ('Dharan', 'Dharan'),
    ('Itahari', 'Itahari'),
    ('Birtamode', 'Birtamode'),
    ('Phidim', 'Phidim'),
    ('Damak', 'Damak'),
    ('Taplejung', 'Taplejung'),
    ('Kakarbhitta', 'Kakarbhitta'),

    # Madhesh Province (Province No. 2)
    ('Janakpur', 'Janakpur'),
    ('Birgunj', 'Birgunj'),
    ('Kalaiya', 'Kalaiya'),
    ('Rajbiraj', 'Rajbiraj'),
    ('Jaleshwar', 'Jaleshwar'),

    # Bagmati Province
    ('Kathmandu', 'Kathmandu'),
    ('Lalitpur', 'Lalitpur'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Hetauda', 'Hetauda'),
    ('Chitwan', 'Chitwan'),
    ('Banepa', 'Banepa'),

    # Gandaki Province
    ('Pokhara', 'Pokhara'),
    ('Baglung', 'Baglung'),
    ('Gorkha', 'Gorkha'),
    ('Damauli', 'Damauli'),
    ('Beni', 'Beni'),

    # Lumbini Province
    ('Butwal', 'Butwal'),
    ('Tansen', 'Tansen'),
    ('Siddharthanagar', 'Siddharthanagar'),
    ('Kapilvastu', 'Kapilvastu'),
    ('Tulsipur', 'Tulsipur'),
    ('Dang', 'Dang'),
    ('Nepalgunj', 'Nepalgunj'),

    # Karnali Province
    ('Surkhet', 'Surkhet'),
    ('Jumla', 'Jumla'),
    ('Dailekh', 'Dailekh'),
    ('Khalanga', 'Khalanga'),

    # Sudurpashchim Province
    ('Dhangadhi', 'Dhangadhi'),
    ('Mahendranagar', 'Mahendranagar'),
    ('Tikapur', 'Tikapur'),
    ('Amargadhi', 'Amargadhi'),
    ('Dadeldhura', 'Dadeldhura'),
    )
class User(AbstractBaseUser):
    email=models.EmailField( max_length=254,unique=True)
    name=models.CharField(max_length=255)
    
    is_active=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_seller=models.BooleanField(default=False)
    is_customer=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD='email'
    objects=UserManager()
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_superuser
    def has_module_perms(self,app_label):
        return self.is_superuser
    

STATE_CHOICES=(
        ('Koshi','Koshi'),
        ('Madhesh','Madhesh'),
        ('Bagmati','Bagmati'), 
        ('Gandaki','Gandaki'),
        ('Lumbini','Lumbini'),
        ('Karnali','Karnali'),
        ('Sudurpaschim','Sudurpaschim'),
    )
CITY_FIELDS = (
    # Province No. 1
    ('Biratnagar', 'Biratnagar'),
    ('Dharan', 'Dharan'),
    ('Itahari', 'Itahari'),
    ('Birtamode', 'Birtamode'),
    ('Phidim', 'Phidim'),
    ('Damak', 'Damak'),
    ('Taplejung', 'Taplejung'),
    ('Kakarbhitta', 'Kakarbhitta'),

    # Madhesh Province (Province No. 2)
    ('Janakpur', 'Janakpur'),
    ('Birgunj', 'Birgunj'),
    ('Kalaiya', 'Kalaiya'),
    ('Rajbiraj', 'Rajbiraj'),
    ('Jaleshwar', 'Jaleshwar'),

    # Bagmati Province
    ('Kathmandu', 'Kathmandu'),
    ('Lalitpur', 'Lalitpur'),
    ('Bhaktapur', 'Bhaktapur'),
    ('Hetauda', 'Hetauda'),
    ('Chitwan', 'Chitwan'),
    ('Banepa', 'Banepa'),

    # Gandaki Province
    ('Pokhara', 'Pokhara'),
    ('Baglung', 'Baglung'),
    ('Gorkha', 'Gorkha'),
    ('Damauli', 'Damauli'),
    ('Beni', 'Beni'),

    # Lumbini Province
    ('Butwal', 'Butwal'),
    ('Tansen', 'Tansen'),
    ('Siddharthanagar', 'Siddharthanagar'),
    ('Kapilvastu', 'Kapilvastu'),
    ('Tulsipur', 'Tulsipur'),
    ('Dang', 'Dang'),
    ('Nepalgunj', 'Nepalgunj'),

    # Karnali Province
    ('Surkhet', 'Surkhet'),
    ('Jumla', 'Jumla'),
    ('Dailekh', 'Dailekh'),
    ('Khalanga', 'Khalanga'),

    # Sudurpashchim Province
    ('Dhangadhi', 'Dhangadhi'),
    ('Mahendranagar', 'Mahendranagar'),
    ('Tikapur', 'Tikapur'),
    ('Amargadhi', 'Amargadhi'),
    ('Dadeldhura', 'Dadeldhura'),
    )
GENDER_CHOICES=(
    ('female','female'),
    ('male','male'),
    ('other','other'),
)
class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    province=models.CharField(max_length=50,choices=STATE_CHOICES)
    city=models.CharField(max_length=50,choices=CITY_FIELDS)
    address=models.CharField(max_length=50)
    landmark=models.CharField(max_length=100,null=True,blank=True)
    phone_number=models.IntegerField()
    gender=models.CharField( max_length=50,choices=GENDER_CHOICES,null=True,blank=True)

CATEGORY_CHOICES=(
    ('skincare','skincare'),
    ('groceries','groceries'),
    ('gadgets','gadgets'),
    ('clothing','clothing'),
    ('winterchildren','winterchildren'),

)
class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=30)
    color=models.CharField(max_length=50,blank=True,null=True)
    product_image=models.ImageField(upload_to='productimg' ,max_length=255, null=True, blank=True)

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
STATUS_CHOICES=(
    ('orderaccepted','orderaccepted'),
    ('packed','packed'),
    ('on the way','on the way'),
    ('Delivered','Delivered'),
    ('cancel','cancel')
)
class Orderplaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')