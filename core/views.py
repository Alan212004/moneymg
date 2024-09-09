
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, F, Case, When, Value, FloatField, ExpressionWrapper
from django.utils import timezone
from .models import Customer, Supplier, STransaction, PTransaction
from .forms import CustomerForm, STransactionForm, PTransactionForm, SupplierForm
from .models import BalanceHistory
from django.db.models import Q

@login_required
def dashboard_view(request):
    # Fetch all customers and suppliers for the logged-in user
    customers = Customer.objects.filter(user=request.user)
    suppliers = Supplier.objects.filter(user=request.user)

    # Calculate today's date
    today = timezone.now().date()

    # Calculate daily debit and credit for the logged-in user's sales transactions
    daily_sales = STransaction.objects.filter(user=request.user, date=today)
    daily_total_amount = daily_sales.aggregate(total=Sum('total_amount'))['total'] or 0
    daily_discount = daily_sales.aggregate(total=Sum('discount'))['total'] or 0
    daily_credit = daily_sales.aggregate(total=Sum('pay_amount'))['total'] or 0

    # Subtract discount and payments to calculate daily debit
    daily_debit = (daily_total_amount - daily_discount) - daily_credit

    # Calculate total debit and credit for the logged-in user's sales transactions
    total_sales = STransaction.objects.filter(user=request.user)
    total_amount = total_sales.aggregate(total=Sum('total_amount'))['total'] or 0
    total_discount = total_sales.aggregate(total=Sum('discount'))['total'] or 0
    total_credit = total_sales.aggregate(total=Sum('pay_amount'))['total'] or 0

    # Subtract discount and payments to calculate total debit
    total_debit = (total_amount - total_discount) - total_credit

    # Calculate total amount for purchase transactions for the logged-in user
    total_purchase_amount = PTransaction.objects.filter(user=request.user).aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate paid amounts (total of pay_amounts in purchase transactions)
    paid_amounts = PTransaction.objects.filter(user=request.user).aggregate(total_paid=Sum('pay_amount'))['total_paid'] or 0

    # Calculate unpaid amounts for suppliers (purchase transactions)
    unpaid_amounts = total_purchase_amount - paid_amounts or 0

    # Fetch recent sales and purchase transactions for the logged-in user
    stransactions = STransaction.objects.filter(user=request.user).order_by('-date')[:5]
    ptransactions = PTransaction.objects.filter(user=request.user).order_by('-date')[:5]

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
    query = request.GET.get('q')  # Get the search query from the request
    sort = request.GET.get('sort', 'name')  # Default sort by 'name'
    
    # Start with customers filtered by the logged-in user
    customers = Customer.objects.filter(user=request.user)
    
    # If a search query is provided, filter customers based on the search input
    if query:
        customers = customers.filter(
            Q(name__icontains=query) |  # Case-insensitive search on name
            Q(nick_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(address__icontains=query)
        )

    # Sort the customers based on the chosen sorting parameter
    if sort.startswith('-'):
        sort_field = sort[1:]
        customers = customers.order_by('-' + sort_field)
    else:
        customers = customers.order_by(sort)
    
    # Render the template with the filtered and sorted customers
    return render(request, 'customers.html', {'customers': customers, 'sort': sort, 'query': query})

# Supplier list view
@login_required
def supplier_list(request):
    query = request.GET.get('q', '')  # Get the search query
    sort = request.GET.get('sort', 'name')  # Default sort by 'name'
    
    # Check if the sort key starts with a minus for descending order
    if sort.startswith('-'):
        sort_field = sort[1:]
        suppliers = Supplier.objects.filter(user=request.user).order_by('-' + sort_field)
    else:
        suppliers = Supplier.objects.filter(user=request.user).order_by(sort)

     # Apply the search filter if a query is provided
    if query:
        suppliers = suppliers.filter(
            Q(name__icontains=query) | 
            Q(phone__icontains=query) |
            Q(address__icontains=query) |
            Q(email__icontains=query)
        )    
    
    return render(request, 'suppliers.html', {'suppliers': suppliers, 'sort': sort, 'query': query})

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
            supplier.user = request.user  # Corrected: Assign the logged-in user
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

            # Apply discount to the total amount
            discounted_amount = max(0, transaction.total_amount - transaction.discount)

            # Calculate balance to be updated based on pay amount
            if transaction.pay_amount < discounted_amount:
                # Partial payment - customer owes the remaining balance
                balance_to_update = discounted_amount - transaction.pay_amount
                customer.balance += balance_to_update
                description = f'Balance increased by {balance_to_update} due to partial payment'

            elif transaction.pay_amount > discounted_amount:
                # Overpayment - customer has credit
                balance_to_update = transaction.pay_amount - discounted_amount
                customer.balance -= balance_to_update
                description = f'Balance decreased by {balance_to_update} due to overpayment'

            else:
                # Exact payment
                balance_to_update = 0
                description = 'Exact payment made, no balance update'

            # Save the customer's updated balance
            customer.save()

            # Create a BalanceHistory entry
            BalanceHistory.objects.create(
                customer=customer,
                amount=transaction.total_amount,
                paid=transaction.pay_amount,
                balance=customer.balance,
                description=description
            )

            # Save the transaction
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
                # Increase the supplier's balance
                unpaid_amount = transaction.total_amount - transaction.pay_amount
                supplier.balance += unpaid_amount
            elif transaction.pay_amount > transaction.total_amount:
                # Decrease the supplier's balance
                excess_payment = transaction.pay_amount - transaction.total_amount
                supplier.balance -= excess_payment
            
            # Save the supplier's updated balance
            supplier.save()
            
            # Save the transaction
            transaction.save()
            
            return redirect('purchase_transactions')
    else:
        form = PTransactionForm(user=request.user)

    return render(request, 'purchase_transactions.html', {
        'form': form,
        'purchase_transactions': purchase_transactions
    })

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
            supplier = form.save(commit=False)
            supplier.user = request.user  # Ensure the user remains the same
            supplier.save()
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


@login_required
def customer_balance_history(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)
    
    # Get the search query from the request
    query = request.GET.get('q', '')

    # Filter the balance history based on the customer and the search query
    history_entries = BalanceHistory.objects.filter(customer=customer)
    
    if query:
        history_entries = history_entries.filter(
            Q(date__icontains=query) |
            Q(amount__icontains=query) |
            Q(paid__icontains=query) |
            Q(balance__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'customer': customer,
        'history_entries': history_entries,
        'query': query,  # Pass the query back to the template
    }
    return render(request, 'customer_balance_history.html', context)