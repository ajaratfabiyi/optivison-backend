import logging
from celery import shared_task
from transactions.models import Transaction
from users.models import User
from decimal import Decimal

logger = logging.getLogger(__name__)

@shared_task
def process_stripe_event(event):
    """
    Handle different Stripe webhook events.
    Ensures idempotency and safe lookups.
    """
    event_type = event.get("type", "")
    data_object = event.get("data", {}).get("object", {})

    logger.info(f"Processing Stripe event: {event_type}")

    if event_type == "checkout.session.completed":
        email = data_object.get("customer_email")
        stripe_id = data_object.get("id")
        amount = Decimal(data_object.get("amount_total", 0)) / 100  # Stripe sends in cents

        try:
            user = User.objects.get(email=email)
            # Prevent duplicate transactions
            if not Transaction.objects.filter(reference=stripe_id).exists():
                Transaction.objects.create(
                    user=user,
                    tx_type="deposit",
                    amount=amount,
                    status="completed",
                    reference=stripe_id
                )
                logger.info(f"Deposit transaction created for user {email}")
            else:
                logger.info(f"Duplicate Stripe event ignored for {stripe_id}")
        except User.DoesNotExist:
            logger.error(f"User with email {email} not found for Stripe event.")

    elif event_type == "payment_intent.payment_failed":
        logger.warning(f"Payment failed: {data_object}")

    else:
        logger.info(f"Unhandled Stripe event type: {event_type}")

    return True
