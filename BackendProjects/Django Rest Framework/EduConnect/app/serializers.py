from rest_framework import serializers
from core.models import Lesson, Assignment, Submission, Course, Module
from django.contrib.auth import get_user_model






class LessonSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'module']
        read_only_fields = ['id']


class AssignmentSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    class Meta:
        model = Assignment
        fields = ['id','title', 'description', 'due_date', 'lesson']
        read_only_fields = ['id']



class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True , read_only=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Module
        fields = ['id', 'title','order','course', 'lessons']
        read_only_fields = ['id']

class CourseSerializer(serializers.ModelSerializer):
    # instructor = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    modules = ModuleSerializer(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id','title', 'description', 'instructor', 'modules']
        read_only_fields = ['id', 'instructor']


class SubmissionSerializer(serializers.ModelSerializer):
    assignment = serializers.PrimaryKeyRelatedField(queryset=Assignment.objects.all())
    # student = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    class Meta:
        model = Submission
        fields = ['id', 'content', 'assignment', 'student']
        read_only_fields = ['id', 'student']