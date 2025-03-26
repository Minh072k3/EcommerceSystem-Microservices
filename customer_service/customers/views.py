from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
import requests
from django.conf import settings
from datetime import datetime, timedelta

from .models import (
    CustomerProfile, RegularCustomer, PremiumCustomer, 
    CorporateCustomer, GuestCustomer, RewardPoint, 
    PremiumBenefit, Invoice
)
from .serializers import (
    CustomerProfileSerializer, RegularCustomerSerializer, 
    PremiumCustomerSerializer, CorporateCustomerSerializer, 
    GuestCustomerSerializer, RewardPointSerializer, 
    PremiumBenefitSerializer, InvoiceSerializer,
    CustomerConversionSerializer, OrderHistorySerializer
)

class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint để quản lý hồ sơ khách hàng.
    """
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Admin, manager, staff có thể xem tất cả
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return CustomerProfile.objects.all()
        # Customer chỉ có thể xem thông tin của chính mình
        return CustomerProfile.objects.filter(user_id=user.id)
    
    # Các phương thức khác giữ nguyên
    
class RegularCustomerViewSet(viewsets.ModelViewSet):
    queryset = RegularCustomer.objects.all()
    serializer_class = RegularCustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Admin, manager, staff có thể xem tất cả
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return RegularCustomer.objects.all()
        # Customer chỉ có thể xem thông tin của chính mình
        return RegularCustomer.objects.filter(profile__user_id=user.id)
    
    # Các phương thức khác giữ nguyên

class PremiumCustomerViewSet(viewsets.ModelViewSet):
    queryset = PremiumCustomer.objects.all()
    serializer_class = PremiumCustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return PremiumCustomer.objects.all()
        return PremiumCustomer.objects.filter(profile__user_id=user.id)
    
    # Các phương thức khác giữ nguyên

class CorporateCustomerViewSet(viewsets.ModelViewSet):
    queryset = CorporateCustomer.objects.all()
    serializer_class = CorporateCustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return CorporateCustomer.objects.all()
        return CorporateCustomer.objects.filter(profile__user_id=user.id)
    
    # Các phương thức khác giữ nguyên

class GuestCustomerViewSet(viewsets.ModelViewSet):
    queryset = GuestCustomer.objects.all()
    serializer_class = GuestCustomerSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # Cho phép tạo khách vãng lai không cần đăng nhập
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return GuestCustomer.objects.none()
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return GuestCustomer.objects.all()
        return GuestCustomer.objects.none()  # Customer thường không cần xem thông tin Guest

class RewardPointViewSet(viewsets.ModelViewSet):
    queryset = RewardPoint.objects.all()
    serializer_class = RewardPointSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return RewardPoint.objects.all()
        # Customer chỉ có thể xem điểm của mình
        try:
            profile = CustomerProfile.objects.get(user_id=user.id)
            regular_customer = RegularCustomer.objects.get(profile=profile)
            return RewardPoint.objects.filter(customer=regular_customer)
        except (CustomerProfile.DoesNotExist, RegularCustomer.DoesNotExist):
            return RewardPoint.objects.none()

class PremiumBenefitViewSet(viewsets.ModelViewSet):
    queryset = PremiumBenefit.objects.all()
    serializer_class = PremiumBenefitSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]  # Chỉ admin/staff có thể chỉnh sửa
        return [permissions.AllowAny()]  # Tất cả có thể xem quyền lợi
    
    def get_queryset(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            user = self.request.user
            if not user.is_authenticated or user.user_type not in ['ADMIN', 'MANAGER', 'STAFF']:
                return PremiumBenefit.objects.none()
        return PremiumBenefit.objects.filter(is_active=True)

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return Invoice.objects.all()
        # Customer chỉ có thể xem hóa đơn của mình
        try:
            profile = CustomerProfile.objects.get(user_id=user.id)
            corporate_customer = CorporateCustomer.objects.get(profile=profile)
            return Invoice.objects.filter(corporate_customer=corporate_customer)
        except (CustomerProfile.DoesNotExist, CorporateCustomer.DoesNotExist):
            return Invoice.objects.none()

class OrderHistoryView(generics.RetrieveAPIView):
    """
    API endpoint để xem lịch sử đơn hàng của khách hàng.
    """
    serializer_class = OrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        customer_id = self.kwargs.get('customer_id')
        user = self.request.user
        
        # Admin, Manager, Staff có thể xem bất kỳ khách hàng nào
        if user.user_type not in ['ADMIN', 'MANAGER', 'STAFF']:
            # Customer chỉ có thể xem của chính mình
            if str(user.id) != str(customer_id):
                self.permission_denied(self.request)
        
        return {'customer_id': customer_id}