from django.contrib import admin
from .models import Product, Sale, SalesItem, Category, Staff, Inventory

# Register your models here.
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SalesItem)
admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(Inventory)