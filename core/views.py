from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from django.utils import timezone
from .models import Customer, Supplier, STransaction, PTransaction
from .forms import CustomerForm, STransactionForm, PTransactionForm, SupplierForm

# Dashboard view
def dashboard_view(request):
    # Fetch all customers and suppliers with their balances
    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()

    # Calculate daily debit and credit using STransaction and PTransaction
    today = timezone.now().date()
    daily_debit = STransaction.objects.filter(date=today).aggregate(Sum('pay_amount'))['pay_amount__sum'] or 0
    daily_credit = PTransaction.objects.filter(date=today).aggregate(Sum('pay_amount'))['pay_amount__sum'] or 0

    # Calculate total debit and credit using STransaction and PTransaction
    total_debit = STransaction.objects.aggregate(Sum('pay_amount'))['pay_amount__sum'] or 0
    total_credit = PTransaction.objects.aggregate(Sum('pay_amount'))['pay_amount__sum'] or 0

    # Fetch recent sales transactions from STransaction and purchase transactions from PTransaction
    stransactions = STransaction.objects.order_by('-date')[:5]
    ptransactions = PTransaction.objects.order_by('-date')[:5]

    context = {
        'customers': customers,
        'suppliers': suppliers,
        'daily_debit': daily_debit,
        'daily_credit': daily_credit,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'stransactions': stransactions,
        'ptransactions': ptransactions,
    }

    return render(request, 'dashboard.html', context)

# Transaction success view
def transaction_success(request):
    return render(request, 'transaction_success.html')

# Customer list view
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})

# Supplier list view
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

# Add customer view
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})

# Sales transactions view
def sales_transactions(request):
    sales_transactions = STransaction.objects.all()
    if request.method == 'POST':
        form = STransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            customer = transaction.customer

            # Update customer's balance if pay amount is less than total
            if transaction.pay_amount < transaction.total_amount:
                balance_to_update = transaction.total_amount - transaction.pay_amount
                customer.balance += balance_to_update
                customer.save()
            elif transaction.pay_amount > transaction.total_amount:
                balance_to_update = transaction.pay_amount - transaction.total_amount
                customer.balance -= balance_to_update
                customer.save()    

            transaction.save()
            return redirect('sales_transactions')
    else:
        form = STransactionForm()
    
    return render(request, 'sales_transactions.html', {'form': form, 'sales_transactions': sales_transactions})

# Purchase transactions view
def purchase_transactions(request):
    purchase_transactions = PTransaction.objects.all()
    if request.method == 'POST':
        form = PTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            supplier = transaction.supplier

            # Update supplier's balance if pay amount is less than total
            if transaction.pay_amount < transaction.total_amount:
                balance_to_update = transaction.total_amount - transaction.pay_amount
                supplier.balance += balance_to_update
                supplier.save()
            elif transaction.pay_amount > transaction.total_amount:
                balance_to_update = transaction.pay_amount - transaction.total_amount
                supplier.balance -= balance_to_update
                supplier.save()    

            transaction.save()
            return redirect('purchase_transactions')
    else:
        form = PTransactionForm()

    return render(request, 'purchase_transactions.html', {'form': form, 'purchase_transactions': purchase_transactions})

# Edit customer view
def edit_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'edit_customer.html', {'form': form})

# Delete customer view
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'confirm_delete.html', {'object': customer})

# Edit supplier view
def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})

# Delete supplier view
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'confirm_delete.html', {'object': supplier})
