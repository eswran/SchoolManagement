
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Classroom
    path('add-classroom/', views.add_classroom, name='add_classroom'),
    path('classrooms/', views.classroom_list, name='classroom_list'),

    # Students
    path('students/', views.student_list, name='student_list'),
    path('add-student/', views.add_student, name='add_student'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),

    # Staffs
    path('staffs/', views.staff_list, name='staff_list'),
]
