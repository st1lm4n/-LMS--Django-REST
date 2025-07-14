from rest_framework import serializers

from .validators import validate_youtube_link
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = self.context['request'].user
        if not user.groups.filter(name='moderators').exists() and self.instance and self.instance.owner != user:
            raise serializers.ValidationError("You can only edit your own courses")
        return data

    class Meta:
        model = Lesson
        fields = '__all__'
        extra_kwargs = {
            'video_link': {'validators': [validate_youtube_link]}
        }


class LessonShortSerializer(serializers.ModelSerializer):

    def validate(self, data):
        user = self.context['request'].user
        if not user.groups.filter(name='moderators').exists() and self.instance and self.instance.owner != user:
            raise serializers.ValidationError("You can only edit your own courses")
        return data

    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "preview", "video_link"]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonShortSerializer(many=True, read_only=True, source="lessons_set")
    lessons_count = serializers.SerializerMethodField()

    def validate(self, data):
        user = self.context['request'].user
        if not user.groups.filter(name='moderators').exists() and self.instance and self.instance.owner != user:
            raise serializers.ValidationError("You can only edit your own courses")
        return data

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count", "lessons"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()
