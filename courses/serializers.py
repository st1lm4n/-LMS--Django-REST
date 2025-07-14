from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_youtube_link


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'course', 'created_at']
        read_only_fields = ['user', 'created_at']


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
    is_subscribed = serializers.SerializerMethodField()

    def validate(self, data):
        user = self.context['request'].user
        if not user.groups.filter(name='moderators').exists() and self.instance and self.instance.owner != user:
            raise serializers.ValidationError("You can only edit your own courses")
        return data

    class Meta:
        model = Course
        fields = ["id", "title", "preview", "description", "lessons_count", "lessons", 'is_subscribed']

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False

    def get_lessons_count(self, obj):
        return obj.lessons.count()
