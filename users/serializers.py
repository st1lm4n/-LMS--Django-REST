from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'city', 'avatar']


class UserDetailSerializer(serializers.ModelSerializer):
    payment_history = PaymentHistorySerializer(many=True, read_only=True, source='payments')

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'city', 'avatar', 'payment_history']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'phone', 'city', 'avatar')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Используем кастомный менеджер для создания пользователя
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            city=validated_data.get('city', ''),
            avatar=validated_data.get('avatar', None)
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_moderator'] = user.groups.filter(name='moderators').exists()
        return token
