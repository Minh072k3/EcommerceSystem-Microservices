from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerProfileViewSet, RegularCustomerViewSet, PremiumCustomerViewSet,
    CorporateCustomerViewSet, GuestCustomerViewSet, RewardPointViewSet,
    PremiumBenefitViewSet, InvoiceViewSet, OrderHistoryView
)

router = DefaultRouter()
router.register(r'profiles', CustomerProfileViewSet)
router.register(r'regular', RegularCustomerViewSet)
router.register(r'premium', PremiumCustomerViewSet)
router.register(r'corporate', CorporateCustomerViewSet)
router.register(r'guest', GuestCustomerViewSet)
router.register(r'rewards', RewardPointViewSet)
router.register(r'benefits', PremiumBenefitViewSet)
router.register(r'invoices', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('order-history/<int:customer_id>/', OrderHistoryView.as_view(), name='order-history'),
]