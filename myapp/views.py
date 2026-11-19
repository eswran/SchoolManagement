
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Classroom, Student, Staff, SchoolProfile
from .forms import ClassroomForm, StudentForm


# ==================================
# HOME / SCHOOL DASHBOARD
# ==================================

def home(request):

    classrooms = Classroom.objects.all()
    class_rooms = classrooms.filter(room_type='class')

    # Actual database student count
    total_students = Student.objects.count()

    # Gender count
    boys_count = Student.objects.filter(gender='Male').count()
    girls_count = Student.objects.filter(gender='Female').count()

    total_teachers = Staff.objects.count()
    school_profile = SchoolProfile.objects.first()
    total_rooms = classrooms.count()
    total_classes = class_rooms.count()

    class_data = []
    highest_students = 0

    for room in class_rooms:
        actual_count = Student.objects.filter(
            classroom=room
        ).count()

        highest_students = max(highest_students, actual_count)

        class_data.append({
            'name': room.room_name,
            'students': actual_count,
        })

    for item in class_data:
        item['percentage'] = (
            item['students'] / highest_students * 100
            if highest_students else 0
        )

    students = Student.objects.select_related('classroom').all()

    context = {
        'classrooms': classrooms,
        'students': students,
        'total_students': total_students,
        'boys_count': boys_count,
        'girls_count': girls_count,
        'total_teachers': total_teachers,
        'total_rooms': total_rooms,
        'total_classes': total_classes,
        'class_data': class_data,
        'highest_students': highest_students,
        'form': ClassroomForm(),
        'school_profile': school_profile,
    }

    return render(request, 'index.html', context)


# ==================================
# ADD CLASSROOM
# ==================================

def add_classroom(request):

    if request.method == 'POST':
        form = ClassroomForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Classroom added successfully!')
            return redirect('add_classroom')
    else:
        form = ClassroomForm()

    classrooms = Classroom.objects.all()

    return render(request, 'myapp/add_classroom.html', {
        'form': form,
        'classrooms': classrooms
    })


# ==================================
# CLASSROOM LIST
# ==================================

def classroom_list(request):

    classrooms = Classroom.objects.all()

    return render(request, 'classrooms.html', {
        'classrooms': classrooms
    })


# ==================================
# STUDENT LIST WITH FILTERS
# ==================================

def student_list(request):

    # Start with all students
    base_students = Student.objects.select_related(
        'classroom'
    ).all()

    # Class filter
    classroom_id = request.GET.get('classroom', '')

    if classroom_id:
        base_students = base_students.filter(
            classroom_id=classroom_id
        )

    # Counts based on selected class (before search/gender filter)
    total_students = base_students.count()
    boys_count = base_students.filter(gender='Male').count()
    girls_count = base_students.filter(gender='Female').count()

    # Search filter
    students = base_students

    search = request.GET.get('search', '').strip()

    if search:
        students = students.filter(
            Q(student_id__icontains=search) |
            Q(student_name__icontains=search) |
            Q(phone__icontains=search)
        )

    # Gender filter
    gender = request.GET.get('gender', '')

    if gender:
        students = students.filter(gender=gender)

    classrooms = Classroom.objects.filter(
        room_type='class'
    ).order_by('id')

    context = {
        'students': students,
        'classrooms': classrooms,
        'search': search,
        'selected_class': classroom_id,
        'selected_gender': gender,
        'total_students': total_students,
        'boys_count': boys_count,
        'girls_count': girls_count,
        'display_count': students.count(),
    }

    return render(request, 'myapp/students.html', context)


# ==================================
# ADD STUDENT WITH CLASS LIMIT
# ==================================

def add_student(request):

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            classroom = form.cleaned_data.get('classroom')

            if not classroom:
                messages.error(
                    request,
                    'Please select a class for this student.'
                )
            else:
                current_count = Student.objects.filter(
                    classroom=classroom
                ).count()

                if current_count >= classroom.student_count:
                    messages.error(
                        request,
                        f'{classroom.room_name} is full! '
                        f'Maximum students: {classroom.student_count}.'
                    )
                else:
                    form.save()

                    messages.success(
                        request,
                        'Student added successfully!'
                    )

                    return redirect('student_list')

    else:
        form = StudentForm()

    return render(request, 'myapp/add_student.html', {
        'form': form
    })


# ==================================
# EDIT STUDENT WITH CLASS LIMIT
# ==================================

def edit_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            new_classroom = form.cleaned_data.get('classroom')

            if not new_classroom:
                messages.error(
                    request,
                    'Please select a class for this student.'
                )
            else:
                current_count = Student.objects.filter(
                    classroom=new_classroom
                ).exclude(id=student.id).count()

                if current_count >= new_classroom.student_count:
                    messages.error(
                        request,
                        f'{new_classroom.room_name} is full! '
                        f'Maximum students: {new_classroom.student_count}.'
                    )
                else:
                    form.save()

                    messages.success(
                        request,
                        'Student details updated successfully!'
                    )

                    return redirect('student_list')

    else:
        form = StudentForm(instance=student)

    return render(request, 'myapp/edit_student.html', {
        'form': form,
        'student': student
    })


# ==================================
# DELETE STUDENT
# ==================================

def delete_student(request, student_id):

    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':

        student.delete()

        messages.success(
            request,
            'Student deleted successfully!'
        )

    return redirect('student_list')


# ==================================
# STAFF LIST
# ==================================

def staff_list(request):
    staffs = Staff.objects.select_related('classroom').all()

    context = {
        'staffs': staffs,
        'total_teachers': staffs.count(),
    }

    return render(request, 'myapp/staffs.html', context)