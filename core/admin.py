from django.contrib import admin
from .models import Customer, Supplier, STransaction, PTransaction

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(STransaction)
admin.site.register(PTransaction)
