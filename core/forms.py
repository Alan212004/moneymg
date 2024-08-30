from django import forms
from .models import Customer
from .models import Transaction
from .models import InventoryTransaction
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'price']


class InventoryTransactionForm(forms.ModelForm):
    class Meta:
        model = InventoryTransaction
        fields = ['product', 'transaction_type', 'quantity', 'date', 'description']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['customer', 'transaction_type', 'amount', 'date', 'description']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']
