from django.contrib import admin
from .models import PromoCode, PromoHistory, Transaction, TransactionHistory, Product, BankAccount


# Register your models here.
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['title', 'benefit', 'quantity', 'code', 'is_expired', 'start_date', 'end_date']
    search_fields = ['code', 'benefit', 'quantity']


admin.site.register(PromoCode, PromoCodeAdmin)


class PromoHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'promo_code', 'prodcut']


admin.site.register(PromoHistory, PromoHistoryAdmin)


class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ['transaction', 'prodcut']


admin.site.register(TransactionHistory, TransactionHistoryAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank_account', 'amount']


admin.site.register(Transaction, TransactionAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']


admin.site.register(Product, ProductAdmin)


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'routing_number', 'holder_name']


admin.site.register(BankAccount, BankAccountAdmin)
