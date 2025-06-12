from rest_framework.permissions import BasePermission


class IsInstructor(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_instructor', False)


class IsStudent(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'is_student', False)