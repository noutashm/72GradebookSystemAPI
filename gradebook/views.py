from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from gradebook.models import *
from gradebook.serializers import *


def index(request):
    return HttpResponse('Hello World')


# class CourseViewset(viewsets.ViewSet):
#     def list(self, request):
#         courses = Course.objects.all()
#         serializer = CourseSerializer(courses, many=True)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = CourseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def retrieve(self, request, pk=None):
#         queryset = Course.objects.all()
#         article = get_object_or_404(queryset, pk=pk)
#         serializer = CourseSerializer(article)
#         return Response(serializer.data)
#
#     def update(self, request, pk=None):
#         course = Course.objects.get(pk=pk)
#         serializer = CourseSerializer(course, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def destroy(self, request, pk=None):
#         course = Course.objects.get(pk=pk)
#         course.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated, IsAdminUser]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]


class StudentEnrolmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrolment.objects.all()
    serializer_class = StudentEnrolmentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # maybe check if user is student or lecturer and return based on that
        groups = self.request.user.group.all()
        if self.request.user.is_superuser:
            studentEnrolments = StudentEnrolment.objects.all()
            return studentEnrolments
        elif groups.filter(name='student').exists():
            student_queryset = self.queryset.filter(student=self.request.user)
            return student_queryset
        elif groups.filter(name='lecturer').exists():
            lecturer_queryset = self.queryset.filter(class1__lecturer=self.request.user)
            return lecturer_queryset

    # TODO: check if lecturer is in this class or not then serializer.save()
    def perform_update(self, serializer):
        groups = self.request.user.group.all()
        if self.request.user.is_superuser or groups.filter(name='lecturer').exists():
            serializer.save()
            return HttpResponse(status=status.HTTP_201_CREATED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]
