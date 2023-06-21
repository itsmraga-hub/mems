from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Order, Loan, OrderItem, Address, Account, Transaction


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Loan)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(Account)
admin.site.register(Transaction)
# admin.site.register()
# admin.site.register()