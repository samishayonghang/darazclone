# Generated by Django 5.1.4 on 2025-01-24 09:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daraz', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('brand', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('skincare', 'skincare'), ('groceries', 'groceries'), ('gadgets', 'gadgets'), ('clothing', 'clothing'), ('winterchildren', 'winterchildren')], max_length=30)),
                ('product_image', models.ImageField(upload_to='productimg')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('province', models.CharField(choices=[('Koshi', 'Koshi'), ('Madhesh', 'Madhesh'), ('Bagmati', 'Bagmati'), ('Gandaki', 'Gandaki'), ('Lumbini', 'Lumbini'), ('Karnali', 'Karnali'), ('Sudurpaschim', 'Sudurpaschim')], max_length=50)),
                ('city', models.CharField(choices=[('Biratnagar', 'Biratnagar'), ('Dharan', 'Dharan'), ('Itahari', 'Itahari'), ('Birtamode', 'Birtamode'), ('Phidim', 'Phidim'), ('Damak', 'Damak'), ('Taplejung', 'Taplejung'), ('Kakarbhitta', 'Kakarbhitta'), ('Janakpur', 'Janakpur'), ('Birgunj', 'Birgunj'), ('Kalaiya', 'Kalaiya'), ('Rajbiraj', 'Rajbiraj'), ('Jaleshwar', 'Jaleshwar'), ('Kathmandu', 'Kathmandu'), ('Lalitpur', 'Lalitpur'), ('Bhaktapur', 'Bhaktapur'), ('Hetauda', 'Hetauda'), ('Chitwan', 'Chitwan'), ('Banepa', 'Banepa'), ('Pokhara', 'Pokhara'), ('Baglung', 'Baglung'), ('Gorkha', 'Gorkha'), ('Damauli', 'Damauli'), ('Beni', 'Beni'), ('Butwal', 'Butwal'), ('Tansen', 'Tansen'), ('Siddharthanagar', 'Siddharthanagar'), ('Kapilvastu', 'Kapilvastu'), ('Tulsipur', 'Tulsipur'), ('Dang', 'Dang'), ('Nepalgunj', 'Nepalgunj'), ('Surkhet', 'Surkhet'), ('Jumla', 'Jumla'), ('Dailekh', 'Dailekh'), ('Khalanga', 'Khalanga'), ('Dhangadhi', 'Dhangadhi'), ('Mahendranagar', 'Mahendranagar'), ('Tikapur', 'Tikapur'), ('Amargadhi', 'Amargadhi'), ('Dadeldhura', 'Dadeldhura')], max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('landmark', models.CharField(blank=True, max_length=100, null=True)),
                ('phone_number', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orderplaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('orderaccepted', 'orderaccepted'), ('packed', 'packed'), ('on the way', 'on the way'), ('Delivered', 'Delivered'), ('cancel', 'cancel')], default='pending', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daraz.customer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daraz.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daraz.product')),
            ],
        ),
    ]
