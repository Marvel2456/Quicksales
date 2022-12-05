from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Product, Sale, SalesItem, Category, Staff, Inventory, LoggedIn, ErrorTicket, Supplier

# Register your models here.


class InventoryHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "product", "status"]
    history_list_display = ["status"]
    search_fields = ['product', 'user__username']



admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SalesItem)
admin.site.register(Category)
admin.site.register(Staff)
admin.site.register(Inventory, InventoryHistoryAdmin)
admin.site.register(LoggedIn)
admin.site.register(ErrorTicket)
admin.site.register(Supplier)