"""
URL configuration for lms_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from courses.views import (
    CourseViewSet,
    LessonViewSet,
    LessonRetrieveUpdateDestroyAPIView,
)
from courses.views import CourseViewSet, LessonViewSet, LessonRetrieveUpdateDestroyAPIView
from users.views import PaymentViewSet, UserViewSet
from users.views import UserRegistrationAPIView, CustomTokenObtainPairView
from users.views import UserViewSet

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"users", UserViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include(('users.urls', 'users'), namespace='users')),
    path('api/courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('api/lessons/', LessonViewSet),
    path('api/lessons/<int:pk>/', LessonRetrieveUpdateDestroyAPIView.as_view()),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegistrationAPIView.as_view(), name='register'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
