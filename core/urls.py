from django.urls import path
from . import views
from .views import customer_balance_history
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('transaction-success/', views.transaction_success, name='transaction_success'),
    path('transactions/sales/', views.sales_transactions, name='sales_transactions'),
    path('transactions/purchase/', views.purchase_transactions, name='purchase_transactions'),

    path('add-customer/', views.add_customer, name='add_customer'),
    path('add-supplier/', views.add_supplier, name='add_supplier'),
    path('add-products/', views.add_product, name='add_product'),
    
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/edit/<int:pk>/', views.edit_customer, name='edit_customer'),  # Edit customer URL
    path('customers/delete/<int:pk>/', views.delete_customer, name='delete_customer'),  # Delete customer URL

    path('products/', views.product_list, name='product_list'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),



    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/edit/<int:pk>/', views.edit_supplier, name='edit_supplier'),  # Edit supplier URL
    path('suppliers/delete/<int:pk>/', views.delete_supplier, name='delete_supplier'),  # Delete supplier URL
    path('customer/<int:customer_id>/balance-history/', customer_balance_history, name='customer_balance_history'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

