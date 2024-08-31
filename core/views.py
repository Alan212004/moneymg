from django.shortcuts import render, redirect
from .models import Supplier
from .models import Transaction, Customer
from django.db import models
from .forms import CustomerForm, TransactionForm




def dashboard(request):
    total_debit = Transaction.objects.filter(transaction_type='D').aggregate(total=models.Sum('amount'))['total'] or 0
    total_credit = Transaction.objects.filter(transaction_type='C').aggregate(total=models.Sum('amount'))['total'] or 0
    transactions = Transaction.objects.all().order_by('-date')[:5]  # Recent transactions
    customers = Customer.objects.all()
    context = {
        'total_debit': total_debit,
        'total_credit': total_credit,
        'transactions': transactions,
        'customers': customers,
    }
    return render(request, 'dashboard.html', context)

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})


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
            return redirect('customer_list')  # Redirect to the customer list page after saving
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})  

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # Redirect to a transaction list view after saving
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})    