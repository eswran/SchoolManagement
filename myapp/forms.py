
from django import forms
from .models import Classroom, Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = [
            'student_name',
            'age',
            'gender',
            'phone',
            'address',
            'classroom',
        ]




class ClassroomForm(forms.ModelForm):

    class Meta:
        model = Classroom
        fields = [
            'room_name',
            'room_type',
            'student_count',
            'teacher_name',
            'teacher_gender',
            'teacher_subject',
            'teacher_qualification',
        ]

        widgets = {
            'room_name': forms.TextInput(attrs={
                'placeholder': 'Enter Room Name'
            }),
        }
