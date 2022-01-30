from django.contrib import admin
from .models import Category, Product, Order, PurchasedItem, Tag

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(PurchasedItem)
admin.site.register(Category)
admin.site.register(Tag)