from rest_framework import serializers
from .models import Course, Lesson


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonShortSerializer(many=True, read_only=True, source='lessons_set')
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        return obj.lessons.count()
