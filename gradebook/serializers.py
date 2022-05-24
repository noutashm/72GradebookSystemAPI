from rest_framework import serializers
from gradebook.models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'staffID', 'firstName', 'lastName', 'email', 'course', 'dateOfBirth']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = ['id', 'studentID', 'firstName', 'lastName', 'email', 'dateOfBirth']


class StudentEnrolmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrolment
        fields = '__all__'