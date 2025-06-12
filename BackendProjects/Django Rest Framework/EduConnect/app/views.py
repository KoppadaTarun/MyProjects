from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer, AssignmentSerializer, SubmissionSerializer
from core.models import Course, Module, Lesson, Assignment, Submission
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from core.permissions import IsInstructor, IsStudent
from rest_framework.permissions import IsAuthenticated



class CourseView(ListCreateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsInstructor()]

        else:
            return [IsAuthenticated()]

    # def get_queryset(self):
    #     return Course.objects.filter(instructor=self.request.user)

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)



class CourseDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsInstructor]



    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        else:
            return [IsInstructor(), IsAuthenticated()]

class CourseEnrollView(APIView):

    permission_classes = [IsAuthenticated, IsStudent]
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        if request.user in course.students.all():
            return Response({'detail': 'Already enrolled.'}, status=status.HTTP_400_BAD_REQUEST)

        course.students.add(request.user)
        return Response({'detail': 'Enrolled successfully.'}, status=status.HTTP_200_OK)





class ModuleView(ListCreateAPIView):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        course_id = self.kwargs.get('course_id')
        course = get_object_or_404(Course, pk=course_id)

        serializer.save(course=course)

    def get_queryset(self):
        course_id = self.kwargs['course_id']

        return Module.objects.filter(course_id= course_id)


class LessonView(ListCreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def peform_create(self, serializer):
        module_id = self.kwargs.get('module_id')
        module = get_object_or_404(Module, pk=module_id)
        serializer.save(module=module)

    def get_queryset(self):
        module_id = self.kwargs.get('module_id')
        return Lesson.objects.filter(module_id=module_id)

class AssignmentView(ListCreateAPIView):

    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        lesson_id = self.kwargs.get('lesson_id')
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        serializer.save(lesson=lesson)

    def get_queryset(self):
        lesson_id = self.kwargs.get('lesson_id')
        return Assignment.objects.filter(lesson_id=lesson_id)

class SubmissionView(ListCreateAPIView):
    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsStudent, IsAuthenticated]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsStudent(), IsAuthenticated()]

        else:
            return [IsInstructor(), IsAuthenticated()]


    def perform_create(self, serializer):
        student = self.request.user
        assignment_id = self.kwargs.get('assignement_id')
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        serializer.save(student=student, assignment=assignment)

    def get_queryset(self):
        asssignment_id = self.kwargs.get('assignement_id')

        return Submission.objects.filter(assignment_id=asssignment_id)








# class CourseView(GenericAPIView, CreateModelMixin, ListModelMixin):
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class CourseDetailView(GenericAPIView,UpdateModelMixin, RetrieveModelMixin,DestroyModelMixin):
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

# class CourseView(APIView):

#     def get(self, request):
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data)

#     def post(self, request):

#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.data)

#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CourseDetailView(APIView):

#     def get(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course)

#         return Response(serializer.data, status=status.HTTP_200_OK)


#     def put(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         serializer = CourseSerializer(course, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, pk):
#         course = get_object_or_404(Course, pk=pk)
#         course.delete()
#         return Response({"message":"Deleted Successfully!"}, status=status.HTTP_204_NO_CONTENT)



