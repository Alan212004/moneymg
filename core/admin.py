from django.contrib import admin
from .models import Customer, Transaction, Supplier, InventoryItem, InventoryTransaction

admin.site.register(Customer)
admin.site.register(Transaction)
admin.site.register(Supplier)
admin.site.register(InventoryItem)
admin.site.register(InventoryTransaction)
