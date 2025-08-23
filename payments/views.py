from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course
from models import Payment
from services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    get_stripe_session,
)


class PaymentCreateView(APIView):
    def post(self, request, course_id):
        course = Course.objects.get(id=course_id)
        user = request.user

        # Создание платежа в Stripe
        product = create_stripe_product(course.title)
        price = create_stripe_price(product.id, course.price)
        session = create_stripe_session(
            price.id,
            success_url="https://yourdomain.com/success/",
            cancel_url="https://yourdomain.com/cancel/",
        )

        # Сохранение платежа в БД
        Payment.objects.create(
            user=user,
            course=course,
            amount=course.price,
            stripe_session_id=session.id,
        )

        return Response({"payment_url": session.url}, status=status.HTTP_201_CREATED)


class PaymentStatusView(APIView):
    def get(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        session = get_stripe_session(payment.stripe_session_id)

        # Обновление статуса
        payment.status = "succeeded" if session.payment_status == "paid" else "pending"
        payment.save()

        return Response({"status": payment.status})
