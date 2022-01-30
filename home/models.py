from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.enums import Choices
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('1', 'Ecommerce'),
        ('2', 'Digital Agency'),
        ('3', 'Other')
    ]

    TOPIC_CHOICES = [
        ('1', 'General'),
        ('2', 'Entreprneurs'),
        ('3', 'Other')
    ]

    

    brand = models.CharField(max_length=100, null=False, blank=False)
    tagline = models.CharField(max_length=100, null=False, blank=False)
    single_price = models.IntegerField()
    multiple_price = models.IntegerField()
    list_price = models.IntegerField()
    extended_price = models.IntegerField()
    exlusive = models.IntegerField(default=0)
    gateway = models.CharField(max_length=50, default='paddle')
    compatibility = models.CharField(max_length=50, blank=True, null=False)
    version = models.DecimalField(decimal_places=2, max_digits=3, blank=False, null=False)
    browser_support = models.CharField(max_length=225, blank=True, null=False)
    layout = models.CharField(max_length=50, blank=True, null=False)
    css_type = models.CharField(max_length=50, blank=True, null=False)
    category = models.CharField(max_length=50, choices= CATEGORY_CHOICES)
    topic = models.CharField(max_length=50, choices= TOPIC_CHOICES)
    tags = models.TextField()
    description = models.TextField()
    link = models.CharField(max_length=225, blank=True, null=False)
    thumbnail = models.ImageField(null=True, blank=True)
    zipfile = models.FileField()
    user = models.CharField(max_length=100)
    orders = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default='pending')


    def __str__(self):
        return self.brand


class Order(models.Model):
    status = models.CharField(max_length=50, default='processed')
    checkout_id = models.CharField(max_length=224)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=224, blank=False, null=False)
    payment = models.DecimalField(decimal_places=2, max_digits=7)
    order_id = models.IntegerField()
    tax = models.CharField(max_length=10)
    receipt_url = models.TextField(blank=False, null=False)
    coupon_code = models.CharField(max_length=20, blank=True, null=True, default='None')
    email = models.EmailField(max_length=224)
    marketing_consent = models.BooleanField(default=False)
    is_subscription = models.BooleanField(default=False)
    dtime = models.DateTimeField(auto_now=True)
    user = models.IntegerField()


    def __str__(self):
        return self.product_name



class PurchasedItem(models.Model):
    product_id = models.CharField(max_length=20)
    user_id = models.IntegerField()
    order_id = models.CharField(max_length=224)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order id " %s"' %self.order_id


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, default=category_name)
    dtime = models.TimeField(auto_now=True)

    def __str__(self):
        return self.category_name



class Tag(models.Model):
    tag_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)
    dtime = models.TimeField(auto_now=True)

    def __str__(self):
        return self.tag_name