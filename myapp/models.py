
from django.db import models


# CLASSROOM MODEL
class Classroom(models.Model):

    ROOM_TYPES = [
        ('class', 'Classroom'),
        ('pet', 'PET Room'),
        ('staff', 'Staff Room'),
        ('computer', 'Computer Lab'),
        ('waste', 'Waste Room'),
    ]

    room_name = models.CharField(max_length=100)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    student_count = models.IntegerField(default=0)

    teacher_name = models.CharField(max_length=100, blank=True)
    teacher_gender = models.CharField(max_length=20, default='Female', blank=True)
    teacher_subject = models.CharField(max_length=100, blank=True)
    teacher_qualification = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.room_name



# STUDENT MODEL
class Student(models.Model):

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        editable=False
    )

    student_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)

        if not self.student_id:
            self.student_id = f"STU{self.pk:04d}"
            super().save(update_fields=['student_id'])
        elif self.pk:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.student_name}"


# STAFF MODEL

class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True)
    staff_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)

    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField(default="", blank=True)

    salary = models.DecimalField(max_digits=10, decimal_places=2)

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members'
    )

    joining_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.staff_id} - {self.staff_name}"

class SchoolProfile(models.Model):
    school_name = models.CharField(max_length=200)
    school_address = models.TextField()
    location = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    telephone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.school_name    
