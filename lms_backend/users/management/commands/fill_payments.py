import random
from datetime import datetime, timedelta
from decimal import Decimal

from courses.models import Course, Lesson
from django.core.management.base import BaseCommand
from users.models import Payment, User


class Command(BaseCommand):
    help = "Fills payments table with test data"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()
        methods = ["cash", "transfer"]

        for _ in range(50):
            user = random.choice(users)
            days_ago = random.randint(1, 365)
            date = datetime.now() - timedelta(days=days_ago)

            # 70% вероятности оплаты курса, 30% - урока
            if random.random() < 0.7 and courses:
                course = random.choice(courses)
                lesson = None
                amount = Decimal(random.uniform(5000, 30000))
            elif lessons:
                course = None
                lesson = random.choice(lessons)
                amount = Decimal(random.uniform(500, 5000))
            else:
                continue

            Payment.objects.create(
                user=user,
                payment_date=date,
                paid_course=course,
                paid_lesson=lesson,
                amount=amount,
                payment_method=random.choice(methods),
            )

        self.stdout.write(self.style.SUCCESS("Successfully created payments"))
