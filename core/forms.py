from django import forms
from .models import Customer, Supplier, STransaction, PTransaction

class STransactionForm(forms.ModelForm):
    class Meta:
        model = STransaction
        fields = ['customer', 'total_amount', 'pay_amount', 'payment_type', 'description']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Expect the user to be passed when initializing the form
        super(STransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['customer'].queryset = Customer.objects.filter(user=user)   

    def clean(self):
        cleaned_data = super().clean()
        customer = cleaned_data.get('customer')

        if not customer:
            self.add_error('customer', 'Customer is required for sale transactions.')

        return cleaned_data

class PTransactionForm(forms.ModelForm):
    class Meta:
        model = PTransaction
        fields = ['supplier', 'total_amount', 'pay_amount', 'payment_type', 'description']
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Expect the user to be passed when initializing the form
        super(PTransactionForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['supplier'].queryset = Supplier.objects.filter(user=user)
            
    def clean(self):
        cleaned_data = super().clean()
        supplier = cleaned_data.get('supplier')

        if not supplier:
            self.add_error('supplier', 'Supplier is required for purchase transactions.')

        return cleaned_data

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'nick_name', 'phone', 'gender', 'email', 'address']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'email']
