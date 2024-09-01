from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F, Case, When, Value, FloatField, ExpressionWrapper
from django.utils import timezone
from .models import Customer, Supplier, STransaction, PTransaction
from .forms import CustomerForm, STransactionForm, PTransactionForm, SupplierForm

def dashboard_view(request):
    # Fetch all customers and suppliers
    customers = Customer.objects.all()
    suppliers = Supplier.objects.all()

    # Calculate today's date
    today = timezone.now().date()

    # Calculate daily debit and credit using STransaction (Sales Transactions only)
    daily_credit = STransaction.objects.filter(date=today).aggregate(total=Sum('pay_amount'))['total'] or 0
    daily_debit = (STransaction.objects.filter(date=today).aggregate(total=Sum('total_amount'))['total'] or 0) - daily_credit

    # Calculate total debit and credit using STransaction (Sales Transactions only)
    total_credit = STransaction.objects.aggregate(total=Sum('pay_amount'))['total'] or 0
    total_debit = (STransaction.objects.aggregate(total=Sum('total_amount'))['total'] or 0) - total_credit

      # Calculate total amount for purchase transactions
    total_purchase_amount = PTransaction.objects.aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate paid amounts (total of pay_amounts in purchase transactions)
    paid_amounts = PTransaction.objects.aggregate(total_paid=Sum('pay_amount'))['total_paid'] or 0

    # Calculate unpaid amounts for suppliers (purchase transactions)
    unpaid_amounts = total_purchase_amount - paid_amounts or  0

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
        'total_purchase_amount': total_purchase_amount,
        'unpaid_amounts': unpaid_amounts,
        'paid_amounts': paid_amounts,
        'stransactions': stransactions,
        'ptransactions': ptransactions,
    }

    return render(request, 'dashboard.html', context)

# Transaction success view
def transaction_success(request):
    return render(request, 'transaction_success.html')

# Customer list view
def customer_list(request):
    sort = request.GET.get('sort', 'name')  # Default sort by 'name'
    if sort.startswith('-'):
        sort_field = sort[1:]
        customers = Customer.objects.all().order_by('-' + sort_field)
    else:
        customers = Customer.objects.all().order_by(sort)
    
    return render(request, 'customers.html', {'customers': customers, 'sort': sort})

# Supplier list view
def supplier_list(request):
    sort = request.GET.get('sort', 'name')  # Default sort by 'name'
    
    # Check if the sort key starts with a minus for descending order
    if sort.startswith('-'):
        suppliers = Supplier.objects.all().order_by(sort)
    else:
        suppliers = Supplier.objects.all().order_by(sort)
    
    return render(request, 'supplier_list.html', {'suppliers': suppliers, 'sort': sort})

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

def purchase_transactions(request):
    purchase_transactions = PTransaction.objects.all()
    if request.method == 'POST':
        form = PTransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            supplier = transaction.supplier

            # Calculate unpaid amount or excess payment
            if transaction.pay_amount < transaction.total_amount:
                # If paid amount is less than the total, increase the supplier's balance
                unpaid_amount = transaction.total_amount - transaction.pay_amount
                supplier.balance += unpaid_amount
            elif transaction.pay_amount > transaction.total_amount:
                # If paid amount is more than the total, decrease the supplier's balance
                excess_payment = transaction.pay_amount - transaction.total_amount
                supplier.balance -= excess_payment
            # If pay_amount is equal to total_amount, no change to supplier's balance

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
