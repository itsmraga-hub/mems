from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Order, Loan, OrderItem, Address, Account, Transaction


class ProductAdmin(admin.ModelAdmin):
    list_display =['id', 'name', 'price', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    list_display =['id', 'client', 'confirmed', 'status', 'paid']


class LoanAdmin(admin.ModelAdmin):
    list_display =['id', 'borrower', 'amount', 'interest_rate']


class OrderItemAdmin(admin.ModelAdmin):
    list_display =['id', 'order', 'product', 'quantity', 'price']




# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Address)
admin.site.register(Account)
admin.site.register(Transaction)
# admin.site.register()
# admin.site.register()