from django.db import models
from django.utils import timezone
import uuid

class CustomerProfile(models.Model):
    CUSTOMER_TYPE_CHOICES = (
        ('REGULAR', 'Regular Customer'),
        ('PREMIUM', 'Premium Customer'),
        ('CORPORATE', 'Corporate Customer'),
        ('GUEST', 'Guest Customer'),
    )

    user_id = models.IntegerField(unique=True, null=True, blank=True)  # Link đến User Service
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPE_CHOICES, default='REGULAR')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_customer_type_display()})"

    class Meta:
        db_table = 'customer_profiles'
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'

class RegularCustomer(models.Model):
    LOYALTY_LEVEL_CHOICES = (
        ('BRONZE', 'Bronze'),
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
    )

    profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='regular_profile')
    loyalty_level = models.CharField(max_length=10, choices=LOYALTY_LEVEL_CHOICES, default='BRONZE')
    total_points = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.profile.full_name} - {self.get_loyalty_level_display()}"
    
    class Meta:
        db_table = 'regular_customers'
        verbose_name = 'Regular Customer'
        verbose_name_plural = 'Regular Customers'

class PremiumCustomer(models.Model):
    MEMBERSHIP_TIER_CHOICES = (
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
        ('DIAMOND', 'Diamond'),
    )

    profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='premium_profile')
    membership_tier = models.CharField(max_length=10, choices=MEMBERSHIP_TIER_CHOICES, default='SILVER')
    membership_id = models.CharField(max_length=50, unique=True)
    start_date = models.DateField(default=timezone.now)
    expire_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.profile.full_name} - {self.get_membership_tier_display()}"
    
    class Meta:
        db_table = 'premium_customers'
        verbose_name = 'Premium Customer'
        verbose_name_plural = 'Premium Customers'

class CorporateCustomer(models.Model):
    profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='corporate_profile')
    company_name = models.CharField(max_length=200)
    tax_id = models.CharField(max_length=50, unique=True)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_terms = models.IntegerField(default=30)  # Số ngày
    billing_address = models.TextField(blank=True, null=True)
    contract_start_date = models.DateField(default=timezone.now)
    contract_end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.company_name} ({self.profile.full_name})"
    
    class Meta:
        db_table = 'corporate_customers'
        verbose_name = 'Corporate Customer'
        verbose_name_plural = 'Corporate Customers'

class GuestCustomer(models.Model):
    profile = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='guest_profile')
    session_id = models.UUIDField(default=uuid.uuid4, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    browser_info = models.CharField(max_length=255, blank=True, null=True)
    converted_to_regular = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Guest - {self.session_id}"
    
    class Meta:
        db_table = 'guest_customers'
        verbose_name = 'Guest Customer'
        verbose_name_plural = 'Guest Customers'

class RewardPoint(models.Model):
    SOURCE_CHOICES = (
        ('PURCHASE', 'Purchase'),
        ('REFERRAL', 'Referral'),
        ('REVIEW', 'Product Review'),
        ('SIGNUP', 'Sign Up Bonus'),
        ('PROMOTION', 'Promotion'),
    )

    customer = models.ForeignKey(RegularCustomer, on_delete=models.CASCADE, related_name='reward_points')
    points = models.IntegerField()
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES)
    reference_id = models.CharField(max_length=100, blank=True, null=True)  # Order ID, etc.
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.customer.profile.full_name} - {self.points} points ({self.get_source_display()})"
    
    class Meta:
        db_table = 'reward_points'
        verbose_name = 'Reward Point'
        verbose_name_plural = 'Reward Points'

class PremiumBenefit(models.Model):
    TIER_CHOICES = (
        ('SILVER', 'Silver'),
        ('GOLD', 'Gold'),
        ('PLATINUM', 'Platinum'),
        ('DIAMOND', 'Diamond'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    required_tier = models.CharField(max_length=10, choices=TIER_CHOICES)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_required_tier_display()})"
    
    class Meta:
        db_table = 'premium_benefits'
        verbose_name = 'Premium Benefit'
        verbose_name_plural = 'Premium Benefits'

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELED', 'Canceled'),
    )
    
    corporate_customer = models.ForeignKey(CorporateCustomer, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    notes = models.TextField(blank=True, null=True)
    reference_order_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.corporate_customer.company_name}"
    
    class Meta:
        db_table = 'corporate_invoices'
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'