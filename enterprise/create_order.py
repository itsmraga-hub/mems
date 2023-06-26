from django.http import HttpResponse

import json
import uuid

from .models import Order, OrderItem

class CreateOrder:
  def __init__(self):
    pass

  def create_new_order(user, payment_method, total_amount, shipping_address, selected_products):
    try:
      order_code = str(uuid.uuid4())
      order = Order.objects.create(
        order_code=order_code,
        confirmed=True,
        client=user,
        total_amount=total_amount,
        payment_method=payment_method,
        shipping_address=shipping_address
      )
      try:
        for selected_product in selected_products:
          item = OrderItem.objects.create(
            order=order,
            product=selected_product,
            quantity=selected_product.client_quantity,
            price=selected_product.price
          )
      except Exception as e:
        return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))
      return HttpResponse(json.dumps({"status": "success", "data": {"message": order_id}}))
    except Exception as e:
      return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))
