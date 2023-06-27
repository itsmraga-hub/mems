from django.shortcuts import get_object_or_404
from .models import Order
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.conf import settings

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
  ipn = sender
  if ipn.payment_status == 'Completed':
    order = get_object_or_404(Order, order_code=ipn.invoice)
    order.paid_amount = ipn.mc_gross

    if ipn.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
      return

    if order.total_cost() == ipn.mc_gross and ipn.mc_currency == 'USD':
      order.paid = True
    
    order.save()