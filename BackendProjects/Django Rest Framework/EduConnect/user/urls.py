from rest_framework.urls import path
from .views import RegisterInstructorView, RegisterStudentView, AuthTokenView

urlpatterns = [
    path('instructor/register/', RegisterInstructorView.as_view(), name='register_user'),
    path('student/register/', RegisterStudentView.as_view(), name='register_student'),
    path('login/', AuthTokenView.as_view(), name='token')
]