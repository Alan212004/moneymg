from django.contrib import admin
from .models import Customer, Supplier, STransaction, PTransaction, Product



class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'user', 'balance')
    list_filter = ('user',)

admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(STransaction)
admin.site.register(PTransaction)