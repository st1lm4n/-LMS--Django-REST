from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    preview = models.ImageField(upload_to="course_previews/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='courses_owned'
    )
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to="lesson_previews/", blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True,
        related_name='lessons_owned'
    )
    permission_classes = [IsAuthenticated, IsModeratorOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
