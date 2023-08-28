from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from advertisements.models import AdvertisementStatusChoices


class IsOwnerOrUpdateAndDeleteRestricted(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if (request.method in ('PATCH','DELETE') and
            request.user != obj.creator and
            not request.user.is_superuser):
            return False
        return True
    
class IsOwnerOrAccessToDraftRestricted(BasePermission):
    def has_object_permission(self, request: Request, view, obj):
        if obj.status == AdvertisementStatusChoices.DRAFT:
            if (request.user != obj.creator and
                not request.user.is_superuser):
                return False
        return True