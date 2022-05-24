from django.contrib import admin
from gradebook.models import *

admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Lecturer)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(StudentEnrolment)