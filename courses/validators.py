from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_youtube_link(value):
    """Проверяет, что ссылка ведет только на YouTube"""
    if value:
        parsed_url = urlparse(value)

        # Проверяем домен
        if parsed_url.netloc not in ["www.youtube.com", "youtube.com", "youtu.be"]:
            raise ValidationError("Допустимы только ссылки на YouTube")

        # Дополнительная проверка для youtu.be (короткие ссылки)
        if parsed_url.netloc == "youtu.be" and not parsed_url.path.strip("/"):
            raise ValidationError("Некорректная ссылка на YouTube")
