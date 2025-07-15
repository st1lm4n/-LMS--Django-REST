from django.urls import path

from .views import LessonRetrieveUpdateDestroyAPIView
from .views import SubscriptionAPIView

app_name = 'courses'  # Добавьте эту строку

from rest_framework.routers import DefaultRouter
from .views import LessonViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
                  path('lessons/', LessonViewSet, name='lesson-list'),
                  path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view(), name='lesson-detail'),
                  path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions'),
              ] + router.urls
