from celery import shared_task
from django.core.mail import send_mail

from courses.models import Subscription


# subscriptions/tasks.py
@shared_task
def send_course_update(course_id):
    from courses.models import Course
    course = Course.objects.get(id=course_id)
    subscriptions = Subscription.objects.filter(course=course, is_active=True)

    # Собираем все email в список
    email_list = [sub.user.email for sub in subscriptions]

    if email_list:
        subject = f"Обновление курса {course.title}"
        message = f"Материалы курса {course.title} были обновлены!"
        send_mail(
            subject,
            message,
            'noreply@lms.ru',
            email_list,  # Отправка одним запросом
            fail_silently=False,
        )
