from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'ADMIN'

class IsManagerUser(permissions.BasePermission):
    """
    Allows access only to manager users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'MANAGER'

class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'STAFF'

class IsCustomerUser(permissions.BasePermission):
    """
    Allows access only to customer users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'CUSTOMER'

class IsAdminOrManager(permissions.BasePermission):
    """
    Allows access to admin or manager users.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and 
            request.user.user_type in ['ADMIN', 'MANAGER']
        )

class IsAdminOrManagerOrStaff(permissions.BasePermission):
    """
    Allows access to admin, manager, or staff users.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and 
            request.user.user_type in ['ADMIN', 'MANAGER', 'STAFF']
        )

class IsOwnerOrAdminOrStaff(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Đọc quyền được cho phép cho bất kỳ yêu cầu nào
        if request.method in permissions.SAFE_METHODS:
            if request.user.user_type in ['ADMIN', 'MANAGER', 'STAFF']:
                return True
            return obj.id == request.user.id

        # Kiểm tra quyền cho những hành động không được đảm bảo an toàn
        if request.user.user_type == 'ADMIN':
            # Admin có thể chỉnh sửa thông tin người dùng là admin, manager, staff
            return obj.user_type in ['ADMIN', 'MANAGER', 'STAFF']
        elif request.user.user_type == 'MANAGER':
            # Manager có thể chỉnh sửa thông tin người dùng là staff, customer
            return obj.user_type in ['STAFF', 'CUSTOMER']
        elif request.user.user_type == 'STAFF':
            # Staff chỉ có thể chỉnh sửa thông tin người dùng là customer
            return obj.user_type == 'CUSTOMER'
        elif request.user.user_type == 'CUSTOMER':
            # Customer chỉ có thể chỉnh sửa thông tin của chính mình
            return obj.id == request.user.id
        
        return False