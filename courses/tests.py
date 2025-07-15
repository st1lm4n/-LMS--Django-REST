import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lms_backend.settings")
django.setup()
import uuid
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from courses.models import Course, Lesson, Subscription


class BaseTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем группы с проверкой существования
        cls.moderator_group, created = Group.objects.get_or_create(name='moderators')

        # Создаем пользователей с уникальными email
        cls.user = User.objects.create_user(
            email=f'user_{uuid.uuid4()}@example.com',
            password='password'
        )
        cls.moderator = User.objects.create_user(
            email=f'moderator_{uuid.uuid4()}@example.com',
            password='password'
        )
        cls.moderator.groups.add(cls.moderator_group)

        # Создаем курс
        cls.course = Course.objects.create(
            title='Test Course',
            description='Test Course Description',
            owner=cls.user
        )

        # Создаем урок
        cls.lesson = Lesson.objects.create(
            course=cls.course,
            title='Test Lesson',
            description='Test Lesson Description',
            owner=cls.user
        )


class CourseTestCase(BaseTestCase):
    def test_course_create(self):
        """Тест создания курса"""
        url = reverse('courses:course-list')
        data = {
            'title': 'New Course',
            'description': 'New Course Description'
        }

        # Анонимный пользователь
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_list(self):
        """Тест получения списка курсов"""
        url = reverse('courses:course-list')

        # Анонимный пользователь
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Аутентифицированный пользователь
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_course_detail(self):
        """Тест детального просмотра курса"""
        url = reverse('courses:course-detail', args=[self.course.id])

        # Анонимный пользователь
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Владелец курса
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Test Course')

        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update(self):
        """Тест обновления курса"""
        url = reverse('courses:course-detail', args=[self.course.id])
        data = {'title': 'Updated Course Title'}

        # Анонимный пользователь
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь (не владелец)
        other_user = User.objects.create_user(
            email=f'other_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Владелец курса
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Course Title')

        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_delete(self):
        """Тест удаления курса"""
        url = reverse('courses:course-detail', args=[self.course.id])

        # Анонимный пользователь
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь (не владелец)
        other_user = User.objects.create_user(
            email=f'other_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Владелец курса
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(BaseTestCase):
    def test_lesson_create(self):
        """Тест создания урока"""
        url = reverse('courses:lesson-list')
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'New Lesson Description'
        }

        # Анонимный пользователь
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_list(self):
        """Тест получения списка уроков"""
        url = reverse('courses:lesson-list')

        # Анонимный пользователь
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Аутентифицированный пользователь
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)

    def test_lesson_detail(self):
        """Тест детального просмотра урока"""
        url = reverse('courses:lesson-detail', args=[self.lesson.id])

        # Анонимный пользователь
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Владелец урока
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['title'], 'Test Lesson')

        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        """Тест обновления урока"""
        url = reverse('courses:lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Lesson Title'}

        # Анонимный пользователь
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь (не владелец)
        other_user = User.objects.create_user(
            email=f'other_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Владелец урока
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson Title')

        # Модератор
        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_delete(self):
        """Тест удаления урока"""
        url = reverse('courses:lesson-detail', args=[self.lesson.id])

        # Анонимный пользователь
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь (не владелец)
        other_user = User.objects.create_user(
            email=f'other_{uuid.uuid4()}@example.com',
            password='password'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Владелец урока
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(BaseTestCase):
    def test_subscription_create_delete(self):
        """Тест создания и удаления подписки"""
        url = reverse('courses:subscription-list')
        data = {'course': self.course.id}

        # Анонимный пользователь
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Аутентифицированный пользователь
        self.client.force_authenticate(user=self.user)

        # Создаем подписку
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        # Удаляем подписку
        response = self.client.delete(url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




class ModelTestCase(BaseTestCase):
    def test_course_str(self):
        """Тест строкового представления курса"""
        self.assertEqual(str(self.course), 'Test Course')

    def test_lesson_str(self):
        """Тест строкового представления урока"""
        self.assertEqual(str(self.lesson), 'Test Lesson')

    def test_subscription_str(self):
        """Тест строкового представления подписки"""
        subscription = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )
        expected_str = f'{self.user} подписан на {self.course}'
        self.assertEqual(str(subscription), expected_str)
