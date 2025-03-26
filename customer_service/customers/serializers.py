from rest_framework import serializers
from .models import (
    CustomerProfile, RegularCustomer, PremiumCustomer, 
    CorporateCustomer, GuestCustomer, RewardPoint, 
    PremiumBenefit, Invoice
)

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'
        read_only_fields = ('user_id', 'created_at', 'updated_at')

class RegularCustomerSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer()
    
    class Meta:
        model = RegularCustomer
        fields = ('id', 'profile', 'loyalty_level', 'total_points')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile_data['customer_type'] = 'REGULAR'
        
        profile = CustomerProfile.objects.create(**profile_data)
        regular_customer = RegularCustomer.objects.create(profile=profile, **validated_data)
        
        return regular_customer
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class PremiumCustomerSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer()
    
    class Meta:
        model = PremiumCustomer
        fields = ('id', 'profile', 'membership_tier', 'membership_id', 'start_date', 'expire_date', 'auto_renew')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile_data['customer_type'] = 'PREMIUM'
        
        profile = CustomerProfile.objects.create(**profile_data)
        premium_customer = PremiumCustomer.objects.create(profile=profile, **validated_data)
        
        return premium_customer
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class CorporateCustomerSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer()
    
    class Meta:
        model = CorporateCustomer
        fields = ('id', 'profile', 'company_name', 'tax_id', 'business_type', 'credit_limit', 
                 'payment_terms', 'billing_address', 'contract_start_date', 'contract_end_date')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile_data['customer_type'] = 'CORPORATE'
        
        profile = CustomerProfile.objects.create(**profile_data)
        corporate_customer = CorporateCustomer.objects.create(profile=profile, **validated_data)
        
        return corporate_customer
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class GuestCustomerSerializer(serializers.ModelSerializer):
    profile = CustomerProfileSerializer()
    
    class Meta:
        model = GuestCustomer
        fields = ('id', 'profile', 'session_id', 'ip_address', 'browser_info', 'converted_to_regular')
        read_only_fields = ('session_id', 'converted_to_regular')
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile_data['customer_type'] = 'GUEST'
        
        profile = CustomerProfile.objects.create(**profile_data)
        guest_customer = GuestCustomer.objects.create(profile=profile, **validated_data)
        
        return guest_customer

class RewardPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardPoint
        fields = '__all__'
        read_only_fields = ('created_at',)

class PremiumBenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumBenefit
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class CustomerConversionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=100)
    
    def validate(self, attrs):
        # Verify user exists in User Service
        # This would be implemented with an API call to User Service
        return attrs

class OrderHistorySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    # Fields that would come from Order Service
    order_count = serializers.IntegerField(read_only=True)
    total_spent = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    orders = serializers.ListField(child=serializers.DictField(), read_only=True)