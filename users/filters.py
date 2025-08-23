import django_filters

from payments.models import Payment


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
    course = django_filters.NumberFilter(field_name="course__id", label="Course ID")
    lesson = django_filters.NumberFilter(field_name="lesson__id", label="Lesson ID")
    payment_method = django_filters.CharFilter(
        field_name="payment_method", lookup_expr="iexact"
    )

    class Meta:
        model = Payment
        fields = ["payment_date", "amount", "payment_method", "course", "lesson"]
