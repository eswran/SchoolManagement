
from django.contrib import admin
from .models import Classroom, Student, Staff


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = (
        'room_name',
        'room_type',
        'student_count',
        'teacher_name'
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'student_name',
        'age',
        'gender',
        'classroom'
    )
    search_fields = ('student_id', 'student_name')
    list_filter = ('gender', 'classroom')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        'staff_id',
        'staff_name',
        'designation',
        'department',
        'salary'
    )
    search_fields = ('staff_id', 'staff_name')
    list_filter = ('department', 'designation')
