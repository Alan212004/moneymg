from django.contrib import admin
from .models import (
    Customer, Supplier, STransaction, PTransaction, Product,
    ExpenseCategory, MoneyTransaction, Budget, SplitGroup, GroupMember, GroupExpense, GroupExpenseShare
)



class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'user', 'balance')
    list_filter = ('user',)

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(STransaction)
admin.site.register(PTransaction)
admin.site.register(ExpenseCategory)
admin.site.register(MoneyTransaction)
admin.site.register(Budget)
admin.site.register(SplitGroup)
admin.site.register(GroupMember)
admin.site.register(GroupExpense)
admin.site.register(GroupExpenseShare)
