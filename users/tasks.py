from celery import shared_task
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone

User = get_user_model()


@shared_task
def check_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)
    count = inactive_users.update(is_active=False)
    return f"Заблокировано пользователей: {count}"
