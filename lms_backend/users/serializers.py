from rest_framework import serializers

from .models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class PaymentHistorySerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="paid_course.title", read_only=True)
    lesson_title = serializers.CharField(source="paid_lesson.title", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_date",
            "course_title",
            "lesson_title",
            "amount",
            "payment_method",
        ]


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentHistorySerializer(
        many=True, read_only=True, source="payments"
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
            "payment_history",
        ]
