
from django.core.management.base import BaseCommand
from myapp.models import Classroom


class Command(BaseCommand):
    help = "Load 15 school rooms and 486 students"

    def handle(self, *args, **kwargs):

        rooms = [
            ("1st Standard", "class", 26, "Priya", "English"),
            ("2nd Standard", "class", 30, "Kavitha", "Tamil"),
            ("3rd Standard", "class", 33, "Revathi", "Maths"),
            ("4th Standard", "class", 38, "Divya", "Science"),
            ("5th Standard", "class", 36, "Meena", "English"),
            ("6th Standard", "class", 40, "Nandhini", "Maths"),
            ("7th Standard", "class", 44, "Lakshmi", "Science"),
            ("8th Standard", "class", 40, "Swetha", "English"),
            ("9th Standard", "class", 45, "Deepa", "Tamil"),
            ("10th Standard", "class", 49, "Anitha", "Maths"),
            ("11th Standard", "class", 50, "Gayathri", "Physics"),
            ("12th Standard", "class", 55, "Sangeetha", "Chemistry"),
            ("PET Room", "pet", 0, "", ""),
            ("Staff Room", "staff", 0, "", ""),
            ("Computer Lab", "computer", 0, "", ""),
        ]

        for name, room_type, count, teacher, subject in rooms:
            Classroom.objects.update_or_create(
                room_name=name,
                defaults={
                    "room_type": room_type,
                    "student_count": count,
                    "teacher_name": teacher,
                    "teacher_gender": "Female" if teacher else "",
                    "teacher_subject": subject,
                    "teacher_qualification": "B.Ed" if teacher else "",
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully loaded 15 rooms and 486 students!"
            )
        )
