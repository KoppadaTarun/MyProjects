"""
Models for the projcets
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError("User must have a email!")
        user = self.model(email=self.normalize_email(email), **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_super_user(self, email, password):
        user =self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User Model"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='courses_created')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_courses', blank=True)

    def __str__(self):
        return self.title


class Module(models.Model):
    title = models.CharField(max_length=300)
    order = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=300)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=300)
    due_date = models.DateField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')

class Submission(models.Model):
    content = models.TextField(max_length=300)
    submitted_at = models.DateField(auto_now_add=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')

