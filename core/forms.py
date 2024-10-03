from django import forms
from .models import Customer, Supplier, STransaction, PTransaction
from django.core.exceptions import ValidationError
from .models import BalanceHistory
from .models import Product

class BalanceHistoryForm(forms.ModelForm):
    class Meta:
        model = BalanceHistory
        fields = ['amount', 'paid', 'balance', 'description']
        
class STransactionForm(forms.ModelForm):
    class Meta:
        model = STransaction
        fields = ['customer', 'total_amount', 'pay_amount', 'discount', 'payment_type', 'description']

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

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'image', 'name', 'print_name', 'hsn_code', 'category','mrp',
            'purchase_price', 'purchase_quantity', 'purchase_type', 'sales_price',
            'sales_quantity', 'sales_type', 'discount', 'tax',
            'expiry_date', 'description', 'status',
        ] # Or specify fields explicitly if needed
        widgets = {
            'expire_date': forms.DateInput(attrs={'type': 'date'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        mrp = cleaned_data.get('mrp')
        sales_price = cleaned_data.get('sales_price')

        if sales_price and mrp and sales_price > mrp:
            self.add_error('sales_price', 'Sales price cannot exceed MRP.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})




class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone', 'address', 'email']
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(str(phone)) < 10 or len(str(phone)) > 15:
            raise ValidationError('Phone Number Must Be Between 10 and 15 Digits Add The Country Code Is Also Need!')
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and '@' not in email:
            raise ValidationError('Invalid email format. Please enter a valid email address.')
        return email
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2 or len(name) > 100:
            raise ValidationError('Name must be between 2 and 100 characters long.')
        return name
