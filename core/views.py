
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F, Case, When, Value, FloatField, ExpressionWrapper
from django.utils import timezone
from .models import Customer, Supplier, STransaction, PTransaction
from .forms import CustomerForm, STransactionForm, PTransactionForm, SupplierForm

@login_required
def dashboard_view(request):
    # Fetch all customers and suppliers
    customers = Customer.objects.filter(user=request.user)
    suppliers = Supplier.objects.filter(user=request.user)

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
@login_required
def transaction_success(request):
    return render(request, 'transaction_success.html')

# Customer list view
@login_required
def customer_list(request):
    sort = request.GET.get('sort', 'name')  # Default sort by 'name'
    if sort.startswith('-'):
        sort_field = sort[1:]
        customers = Customer.objects.filter(user=request.user).order_by('-' + sort_field)
    else:
        customers = Customer.objects.filter(user=request.user).order_by(sort)
    
    return render(request, 'customers.html', {'customers': customers, 'sort': sort})

# Supplier list view
@login_required
def supplier_list(request):
    sort = request.GET.get('sort', 'name')  # Default sort by 'name'
    
    # Check if the sort key starts with a minus for descending order
    if sort.startswith('-'):
        sort_field = sort[1:]
        suppliers = Supplier.objects.filter(user=request.user).order_by('-' + sort_field)
    else:
        suppliers = Supplier.objects.filter(user=request.user).order_by(sort)
    
    return render(request, 'suppliers.html', {'suppliers': suppliers, 'sort': sort})

# Add customer view
@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user  # Assign the logged-in user
            customer.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})

# Add Supplier view
@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            Supplier.user = request.user  # Assign the logged-in user
            supplier.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()

    return render(request, 'add_supplier.html', {'form': form})

# Sales transactions view
@login_required
def sales_transactions(request):
    sales_transactions = STransaction.objects.filter(user=request.user)

    if request.method == 'POST':
        form = STransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
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
        form = STransactionForm(user=request.user)
    
    return render(request, 'sales_transactions.html', {'form': form, 'sales_transactions': sales_transactions})

@login_required
def purchase_transactions(request):
    purchase_transactions = PTransaction.objects.filter(user=request.user)
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
                supplier.save()
            # If pay_amount is equal to total_amount, no change to supplier's balance

             
            transaction.save()
            return redirect('purchase_transactions')
    else:
        form = PTransactionForm(user=request.user)

    return render(request, 'purchase_transactions.html', {'form': form, 'purchase_transactions': purchase_transactions})

# Edit customer view
@login_required
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
@login_required
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'confirm_delete.html', {'object': customer})

# Edit supplier view
@login_required
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
@login_required
def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'confirm_delete.html', {'object': supplier})

