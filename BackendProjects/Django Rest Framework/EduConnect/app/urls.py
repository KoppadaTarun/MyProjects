from rest_framework.urls import path
from .views import CourseDetailView, CourseView, CourseEnrollView, ModuleView, LessonView, AssignmentView, SubmissionView
urlpatterns = [
    path('courses/', CourseView.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/enroll/', CourseEnrollView.as_view(), name='enroll'),
    path('courses/<int:course_id>/modules/', ModuleView.as_view(), name='modules'),
    path('modules/<int:module_id>/lessons/', LessonView.as_view(), name='lessons'),
    path('lessons/<int:lesson_id>/assignments/', AssignmentView.as_view(), name='assignements'),
    path('assignments/<int:assignement_id>/submit/', SubmissionView.as_view(), name='submissions')

]
