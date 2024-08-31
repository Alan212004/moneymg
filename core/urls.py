from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transaction-success/', views.transaction_success, name='transaction_success'),
    path('transactions/sales/', views.sales_transactions, name='sales_transactions'),
    path('transactions/purchase/', views.purchase_transactions, name='purchase_transactions'),
    path('add-customer/', views.add_customer, name='add_customer'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/edit/<int:pk>/', views.edit_customer, name='edit_customer'),  # Edit customer URL
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),  # Delete customer URL
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/edit/<int:pk>/', views.edit_supplier, name='edit_supplier'),  # Edit supplier URL
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),  # Delete supplier URL
]
