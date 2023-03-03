from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='index'),
    path('update_cart/', views.updateCart, name='update_cart'),
    path('update_quantity/', views.updateQuantity, name='update_quantity'),
    path('cart/', views.cart, name='cart'),
    path('completed/', views.sale_complete, name='completed'),
    path('checkout/', views.checkout, name='checkout'),
    path('category_list/', views.category_list, name='category_list'),
    path('category/<str:pk>/', views.category, name='category'),
    path('edit_category/', views.edit_category, name='edit_category'),
    path('reciept/<str:pk>/', views.reciept, name='reciept'),
    path('category_delete/', views.delete_category, name='category_delete'),
    path('store/', views.store, name='store'),
    path('delete_product/', views.delete_product, name='delete_product'),
    path('sales/', views.sales, name='sales'),
    path('sales<int:pk>/', views.sales, name='sales_single'),
    path('sales_delete/', views.sale_delete, name='sales_delete'),
    path('records/', views.record, name='records'),
    path('products/', views.product_category, name='products'),
    path('product/<str:pk>/', views.product, name='product'),
    path('edit_product/', views.edit_product, name='edit_product'),
    path('set_reorder/', views.edit_inventory, name='set_reorder'),
    path('inventorys/', views.inventory_list, name='inventorys'),
    path('inventory/<str:pk>/', views.inventory, name='inventory'),
    path('delete_inventory/', views.delete_inventory, name='delete_inventory'),
    path('staff/', views.staffs, name='staff'),
    path('staff_detail/<str:pk>/', views.staff, name='staff_detail'),
    path('edit_staff/', views.edit_staff, name='edit_staff'),
    path('delete_staff/', views.delete_staff, name='delete_staff'),
    path('restock/', views.restock, name='restock'),
    path('export_sales', views.export_sales_csv, name= 'export_sales'),
    path('export_audit', views.export_audit_csv, name= 'export_audit'),
    path('profitData/<str:pk>/', views.profitData, name='profitData'),
    path('price_audit/', views.inventoryAudit, name='price_audit'),
    path('ticket/', views.errorTicket, name='ticket'),
    path('create_ticket/', views.createTicket, name='create_ticket'),
    path('tickets/<str:pk>', views.Ticket, name='tickets'),
    path('reports/', views.report, name='reports'),
    path('count/', views.countView, name='count'),
    path('addcount/', views.addCount, name='addcount'),
    path('productlist/', views.inventoryView, name='productlist'),
    path('export_profit_pdf', views.export_profit, name= 'export_profit_pdf'),
]
# what happens when users logs in to another POS and makes sale note: should not be possible
# A business that price varies?
#  work on field for staff to enter price sold
