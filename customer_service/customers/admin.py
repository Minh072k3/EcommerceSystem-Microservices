from django.contrib import admin
from .models import (
    CustomerProfile, RegularCustomer, PremiumCustomer, 
    CorporateCustomer, GuestCustomer, RewardPoint, 
    PremiumBenefit, Invoice
)

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'full_name', 'phone', 'customer_type', 'created_at')
    list_filter = ('customer_type', 'created_at')
    search_fields = ('user_id', 'full_name', 'email', 'phone')

@admin.register(RegularCustomer)
class RegularCustomerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'loyalty_level', 'total_points')
    list_filter = ('loyalty_level',)

@admin.register(PremiumCustomer)
class PremiumCustomerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'membership_tier', 'expire_date')
    list_filter = ('membership_tier',)

@admin.register(CorporateCustomer)
class CorporateCustomerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'company_name', 'credit_limit', 'tax_id')
    search_fields = ('company_name', 'tax_id')

@admin.register(GuestCustomer)
class GuestCustomerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'session_id', 'converted_to_regular')

@admin.register(RewardPoint)
class RewardPointAdmin(admin.ModelAdmin):
    list_display = ('customer', 'points', 'source', 'created_at', 'expires_at')
    list_filter = ('source', 'created_at')

@admin.register(PremiumBenefit)
class PremiumBenefitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'required_tier')
    list_filter = ('required_tier',)

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('corporate_customer', 'invoice_number', 'amount', 'status', 'due_date')
    list_filter = ('status', 'due_date')
    search_fields = ('invoice_number', 'corporate_customer__company_name')