from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    LoginSerializer, CustomerSerializer
)
from .permissions import (
    IsAdminUser, IsManagerUser, IsStaffUser, 
    IsCustomerUser, IsAdminOrManager, 
    IsAdminOrManagerOrStaff, IsOwnerOrAdminOrStaff
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminOrManager]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAdminOrManagerOrStaff]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdminOrStaff]
        elif self.action in ['register', 'login']:
            permission_classes = [permissions.AllowAny]
        elif self.action == 'verify_token':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        # Admin, manager có thể xem tất cả user
        if user.user_type in ['ADMIN', 'MANAGER']:
            return User.objects.all()
        # Staff chỉ có thể xem customer
        elif user.user_type == 'STAFF':
            return User.objects.filter(user_type='CUSTOMER')
        # Customer chỉ có thể xem thông tin của chính mình
        elif user.user_type == 'CUSTOMER':
            return User.objects.filter(id=user.id)
        return User.objects.none()
    
    def create(self, request, *args, **kwargs):
        # Admin chỉ có thể tạo admin, manager, staff
        # Manager chỉ có thể tạo staff, customer
        user_type = request.data.get('user_type', 'CUSTOMER').upper()
        
        if request.user.user_type == 'ADMIN' and user_type not in ['ADMIN', 'MANAGER', 'STAFF']:
            return Response(
                {"detail": "Admin chỉ có thể tạo tài khoản ADMIN, MANAGER, STAFF"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if request.user.user_type == 'MANAGER' and user_type not in ['STAFF', 'CUSTOMER']:
            return Response(
                {"detail": "Manager chỉ có thể tạo tài khoản STAFF, CUSTOMER"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Admin chỉ có thể chỉnh sửa thông tin admin, manager, staff
        if request.user.user_type == 'ADMIN' and instance.user_type not in ['ADMIN', 'MANAGER', 'STAFF']:
            return Response(
                {"detail": "Admin chỉ có thể chỉnh sửa thông tin ADMIN, MANAGER, STAFF"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Manager chỉ có thể chỉnh sửa thông tin staff, customer
        if request.user.user_type == 'MANAGER' and instance.user_type not in ['STAFF', 'CUSTOMER']:
            return Response(
                {"detail": "Manager chỉ có thể chỉnh sửa thông tin STAFF, CUSTOMER"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Staff chỉ có thể chỉnh sửa thông tin customer
        if request.user.user_type == 'STAFF' and instance.user_type != 'CUSTOMER':
            return Response(
                {"detail": "Staff chỉ có thể chỉnh sửa thông tin CUSTOMER"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Customer chỉ có thể chỉnh sửa thông tin của chính mình
        if request.user.user_type == 'CUSTOMER' and instance.id != request.user.id:
            return Response(
                {"detail": "Customer chỉ có thể chỉnh sửa thông tin của chính mình"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Admin chỉ có thể xóa thông tin admin, manager, staff
        if request.user.user_type == 'ADMIN' and instance.user_type not in ['ADMIN', 'MANAGER', 'STAFF']:
            return Response(
                {"detail": "Admin chỉ có thể xóa thông tin ADMIN, MANAGER, STAFF"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Manager chỉ có thể xóa thông tin staff, customer
        if request.user.user_type == 'MANAGER' and instance.user_type not in ['STAFF', 'CUSTOMER']:
            return Response(
                {"detail": "Manager chỉ có thể xóa thông tin STAFF, CUSTOMER"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Staff chỉ có thể xóa thông tin customer
        if request.user.user_type == 'STAFF' and instance.user_type != 'CUSTOMER':
            return Response(
                {"detail": "Staff chỉ có thể xóa thông tin CUSTOMER"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Customer không có quyền xóa
        if request.user.user_type == 'CUSTOMER':
            return Response(
                {"detail": "Customer không có quyền xóa tài khoản"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def verify_token(self, request):
        # Xác thực token là hợp lệ (sẽ được thực hiện bởi JWT middleware)
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'user_type': request.user.user_type
        })


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminOrManagerOrStaff]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAdminOrManagerOrStaff]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsOwnerOrAdminOrStaff]
        elif self.action == 'destroy':
            permission_classes = [IsAdminOrManagerOrStaff]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        # Admin, manager có thể xem tất cả customer
        if user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
            return User.objects.filter(user_type='CUSTOMER')
        # Customer chỉ có thể xem thông tin của chính mình
        elif user.user_type == 'CUSTOMER':
            return User.objects.filter(id=user.id, user_type='CUSTOMER')
        return User.objects.none()
    
    def create(self, request, *args, **kwargs):
        request.data['user_type'] = 'CUSTOMER'
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)