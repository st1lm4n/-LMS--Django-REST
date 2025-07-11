import django_filters

from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(
            ("payment_date", "date_asc"),
            ("-payment_date", "date_desc"),
        ),
        field_labels={
            "payment_date": "По дате (возрастание)",
            "-payment_date": "По дате (убывание)",
        },
    )

    class Meta:
        model = Payment
        fields = {
            "paid_course": ["exact"],
            "paid_lesson": ["exact"],
            "payment_method": ["exact"],
        }
