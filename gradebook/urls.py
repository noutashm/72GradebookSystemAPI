from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from gradebook.views import *

router = DefaultRouter()
router.register('course', CourseViewSet, basename='course')
router.register('semester', SemesterViewSet, basename='semester')
router.register('lecturer', LecturerViewSet, basename='lecturer')
router.register('class', ClassViewSet, basename='class')
router.register('student', StudentViewSet, basename='student')
router.register('student_enrolment', StudentEnrolmentViewSet, basename='student_enrolment')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
]
