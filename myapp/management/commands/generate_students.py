
from django.core.management.base import BaseCommand
from myapp.models import Classroom, Student


class Command(BaseCommand):
    help = "Generate demo students for all 12 standards"

    def handle(self, *args, **kwargs):

        class_data = {
            "1st Standard": 26,
            "2nd Standard": 30,
            "3rd Standard": 33,
            "4th Standard": 38,
            "5th Standard": 36,
            "6th Standard": 40,
            "7th Standard": 44,
            "8th Standard": 40,
            "9th Standard": 45,
            "10th Standard": 49,
            "11th Standard": 50,
            "12th Standard": 55,
        }

        first_names = [
            "Arun", "Kavin", "Ajay", "Vijay",
            "Ragul", "Abi", "Karthik", "Sanjay",
            "Priya", "Divya", "Agalya", "Nila",
            "Kavya", "Anu", "Meena", "Harini",
        ]

        total_created = 0

        for class_name, target_count in class_data.items():

            classroom = Classroom.objects.filter(
                room_name=class_name,
                room_type="class"
            ).first()

            if classroom is None:
                self.stdout.write(
                    self.style.WARNING(f"{class_name} not found")
                )
                continue

            existing_count = Student.objects.filter(
                classroom=classroom
            ).count()

            missing_count = max(0, target_count - existing_count)

            for i in range(missing_count):

                number = existing_count + i
                gender = "Male" if number % 2 == 0 else "Female"

                age = int(
                    class_name.split()[0]
                    .replace("st", "")
                    .replace("nd", "")
                    .replace("rd", "")
                    .replace("th", "")
                ) + 5

                name = (
                    f"{first_names[number % len(first_names)]} "
                    f"Demo {class_name} {number + 1}"
                )

                Student.objects.create(
                    student_name=name,
                    age=age,
                    gender=gender,
                    phone="0000000000",
                    address=f"DEMO ADDRESS - {class_name}",
                    classroom=classroom
                )

                total_created += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"{class_name}: "
                    f"{Student.objects.filter(classroom=classroom).count()} students"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total {total_created} demo students created!"
            )
        )
