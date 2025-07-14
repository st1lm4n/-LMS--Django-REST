from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password'
        )
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='password'
        )
        self.moderator.groups.create(name='moderators')

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

        # Аутентифицируем пользователя
        self.client.force_authenticate(self.user)

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update_owner(self):
        """Тест обновления урока владельцем"""
        url = reverse('courses:lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Title'}

        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Title')

    def test_lesson_update_moderator(self):
        """Тест обновления урока модератором"""
        url = reverse('courses:lesson-detail', args=[self.lesson.id])
        data = {'description': 'Moderator Updated'}

        self.client.force_authenticate(self.moderator)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.description, 'Moderator Updated')

    def test_lesson_delete_not_owner(self):
        """Тест удаления урока не владельцем"""
        url = reverse('courses:lesson-detail', args=[self.lesson.id])

        self.client.force_authenticate(self.moderator)
        response = self.client.delete(url)



class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description'
        )
        self.subscription_url = reverse('courses:subscriptions')

    def test_subscription_create(self):
        """Тест создания подписки"""
        self.client.force_authenticate(self.user)
        data = {'course_id': self.course.id}

        response = self.client.post(self.subscription_url, data)
        self.assertTrue(Subscription.objects.filter(
            user=self.user,
            course=self.course
        ).exists())

    def test_subscription_delete(self):
        """Тест удаления подписки"""
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

        url = reverse('courses:course-detail', args=[self.course.id])
        self.client.force_authenticate(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])