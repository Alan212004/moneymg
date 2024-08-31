from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Supplier, STransaction, PTransaction, Customer
from .forms import CustomerForm, STransactionForm, PTransactionForm
from django.utils import timezone


def dashboard(request):
    # Total Debit and Credit
    total_debit = STransaction.objects.aggregate(total=Sum('pay_amount'))['total'] or 0
    total_credit = PTransaction.objects.aggregate(total=Sum('pay_amount'))['total'] or 0

    # Daily (Today) Debit and Credit
    today = timezone.now().date()
    daily_debit = STransaction.objects.filter(date=today).aggregate(total=Sum('pay_amount'))['total'] or 0
    daily_credit = PTransaction.objects.filter(date=today).aggregate(total=Sum('pay_amount'))['total'] or 0

    # Recent Transactions
    stransactions = STransaction.objects.all().order_by('-date')[:5]
    ptransactions = PTransaction.objects.all().order_by('-date')[:5]

    context = {
        'total_debit': total_debit,
        'total_credit': total_credit,
        'daily_debit': daily_debit,
        'daily_credit': daily_credit,
        'stransactions': stransactions,
        'ptransactions': ptransactions,
    }
    return render(request, 'dashboard.html', context)

def transaction_success(request):
    return render(request, 'transaction_success.html')

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers.html', {'customers': customers})

def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})

def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})

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

            transaction.save()
            return redirect('sales_transactions')
    else:
        form = STransactionForm()
    
    return render(request, 'sales_transactions.html', {'form': form, 'sales_transactions': sales_transactions})

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

            transaction.save()
            return redirect('purchase_transactions')
    else:
        form = PTransactionForm()

    return render(request, 'purchase_transactions.html', {'form': form, 'purchase_transactions': purchase_transactions})

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

def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'confirm_delete.html', {'object': customer})    

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

def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'confirm_delete.html', {'object': supplier})
    
            