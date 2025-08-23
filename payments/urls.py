from django.urls import path
from views import PaymentCreateView, PaymentStatusView

urlpatterns = [
    path("payments/<int:course_id>/", PaymentCreateView.as_view()),
    path("payments/status/<int:payment_id>/", PaymentStatusView.as_view()),
]
