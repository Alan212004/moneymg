from django import forms
from .models import Customer
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['customer', 'transaction_type', 'amount', 'date', 'description']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','nick_name','phone','gender', 'email', 'address']
