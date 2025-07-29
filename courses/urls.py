from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, LessonViewSet, SubscriptionAPIView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscription-list'),
] + router.urls