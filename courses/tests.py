import os
import uuid

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_backend.settings")
django.setup()

from django.urls import reverse
from rest_framework import status
from users.models import User
from courses.models import Course, Lesson, Subscription
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

class LessonTestCase(APITestCase):

    def setUp(self):
        # Создаем группу модераторов
        self.moderator_group, _ = Group.objects.get_or_create(name='moderators')

        # Создаем пользователей
        self.user = User.objects.create_user(
            email=f'user_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.moderator = User.objects.create_user(
            email=f'moderator_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.moderator.groups.add(self.moderator_group)  # Добавляем в группу

        # Создаем курс и уроки
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Test Lesson',
            description='Test Lesson Description',
            owner=self.user
        )

    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse('courses:lesson-list')
        data = {
                'course': self.course.id,
                'title': 'New Lesson',
                'description': 'New Lesson Description'
            }

        self.client.force_authenticate(self.user)
        response = self.client.post(url, data)

        # Должно быть 201 Created, а не 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Дополнительная проверка: убедимся, что урок действительно создан
        lesson = Lesson.objects.get(title='New Lesson')
        self.assertEqual(lesson.description, 'New Lesson Description')

    def test_lesson_create(self):
        """Тест создания урока"""
        url = '/api/courses/lessons/'
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'New Lesson Description'
        }

        # # 1. Проверка без аутентификации
        # self.client.logout()
        # response = self.client.post(url, data)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # # 2. Проверка с обычным пользователем
        # self.client.force_authenticate(self.user)
        # response = self.client.post(url, data)
        # print(response.content)  # Для диагностики
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # 3. Проверка с модератором
        # self.client.force_authenticate(self.moderator)
        # response = self.client.post(url, data)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Для диагностики
        print("Response status:", response.status_code)
        print("Response content:", response.content)



    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором"""
        # Исправленный URL
        url = reverse('courses:lesson-detail', kwargs={'pk': self.lesson.id})
        data = {'description': 'Moderator Updated'}

        self.client.force_authenticate(self.moderator)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.description, 'Moderator Updated')

    def test_lesson_delete_not_owner(self):
        """Тест удаления урока не владельцем"""
        # Исправленный URL
        url = reverse('courses:lesson-detail', kwargs={'pk': self.lesson.id})

        self.client.force_authenticate(self.moderator)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email=f'user_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        # Исправленный URL с namespace
        self.subscription_url = reverse('courses:subscriptions')

    def test_subscription_create(self):
        """Тест создания подписки"""
        self.client.force_authenticate(self.user)
        data = {'course_id': self.course.id}

        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_subscription_delete(self):
        """Тест удаления подписки"""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(self.user)
        data = {'course_id': self.course.id}

        response = self.client.post(self.subscription_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_course_subscription_flag(self):
        """Тест флага подписки в курсе"""
        # Создаем подписку
        Subscription.objects.create(user=self.user, course=self.course)

        # Исправленный URL для деталей курса
        url = reverse('courses:course-detail', kwargs={'pk': self.course.id})
        self.client.force_authenticate(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])
