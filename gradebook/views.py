from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from gradebook.serializers import *


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAuthenticated]


class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        lecturer = self.get_object()
        lecturer.user.delete()
        lecturer.delete()
        return Response(data='Lecturer Deleted Successfully!')


class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        student = self.get_object()
        student.user.delete()
        student.delete()
        return Response(data='Student Deleted Successfully!')


class StudentEnrolmentViewSet(viewsets.ModelViewSet):
    queryset = StudentEnrolment.objects.all()
    serializer_class = StudentEnrolmentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        groups = self.request.user.groups.values_list('name', flat=True)
        if self.request.user.is_superuser:
            studentEnrolments = self.queryset.all()
            return studentEnrolments
        elif 'lecturer' in groups:
            lecturer_queryset = self.queryset.filter(class1__lecturer__user=self.request.user)
            return lecturer_queryset
        elif 'student' in groups:
            student_queryset = self.queryset.filter(student__user=self.request.user)
            return student_queryset

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
            return HttpResponse(status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        groups = self.request.user.groups.values_list('name', flat=True)
        if self.request.user.is_superuser or 'lecturer' in groups:
            serializer.save()
            return HttpResponse(status=status.HTTP_202_ACCEPTED)
        elif 'student' in groups:
            return HttpResponse(status=status.HTTP_401_UNAUTHORIZED)
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'group': user.groups.all()[0].name
        })
