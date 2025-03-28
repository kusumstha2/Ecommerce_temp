# signals.py
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Billing
from decimal import Decimal
from django.db.models import Sum

@receiver(m2m_changed, sender=Billing.purchases.through)
def update_billing_total(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove", "post_clear"]:
        total_sum = instance.purchases.aggregate(total_sum=Sum("total"))["total_sum"] or Decimal("0.00")
        instance.total = total_sum
        instance.save(update_fields=["total"])  # Save the instance with updated total
