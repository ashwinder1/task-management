from rest_framework.permissions import BasePermission

class IsClient(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'client'
    
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'employee'
    
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'

