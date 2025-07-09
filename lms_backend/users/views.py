from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
