from django.shortcuts import render
from .models import Transaction, Customer
from django.db import models

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
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transaction_list.html', {'transactions': transactions})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})
