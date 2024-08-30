from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('customers/', views.customer_list, name='customer_list'),
     path('inventory/', views.inventory_dashboard, name='inventory_dashboard'),
    path('inventory/items/', views.inventory_list, name='inventory_list'),
    path('inventory/suppliers/', views.supplier_list, name='supplier_list'),
    path('add-product/', views.add_product, name='add_product'),
    path('inventory-dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    path('add-inventory-transaction/', views.add_inventory_transaction, name='add_inventory_transaction'),
    path('inventory-transactions/', views.inventory_transaction_list, name='inventory_transaction_list'),

]
