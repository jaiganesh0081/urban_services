from rest_framework.permissions import BasePermission
from .models import Role



class IsProvider(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.role == Role.Provider:
            return True


class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.role == Role.Customer:
            return True