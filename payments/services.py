import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    return stripe.Product.create(name=name)


def create_stripe_price(product_id, amount):
    return stripe.Price.create(
        product=product_id,
        unit_amount=int(amount * 100),  # Конвертация в копейки
        currency='rub',
    )


def create_stripe_session(price_id, success_url, cancel_url):
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{'price': price_id, 'quantity': 1}],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )


def get_stripe_session(session_id):
    return stripe.checkout.Session.retrieve(session_id)
