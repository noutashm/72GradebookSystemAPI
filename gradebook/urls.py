from django.urls import path, include
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
    # path('', index, name='home'),
    # path('course', course_list, name='courses'),
    # path('course', CourseList.as_view(), name='courses'),
    # path('course/<int:pk>', course_details, name='course'),
    # path('course/<int:pk>', CourseDetails.as_view(), name='course'),
    path('', include(router.urls))
]
