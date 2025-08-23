from django.db import models

from .validators import validate_youtube_link


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, related_name="courses_owned"
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_link = models.URLField(
        blank=True, null=True, validators=[validate_youtube_link]  # Добавляем валидатор
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, null=True, related_name="lessons_owned"
    )

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="subscriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")  # Одна подписка на пользователя и курс
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.course}"
