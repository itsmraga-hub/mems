from django.http import HttpResponse

import json
import uuid

from .models import Order, OrderItem, Product

class CreateOrder:
  def __init__(self):
    pass

  def create_new_order(user, payment_method, total_amount, shipping_address, selected_products):
    try:
      order_code = str(uuid.uuid4())
      order = Order.objects.get(id=8)
      try:
        for selected_product in selected_products:
          product = Product.objects.get(id=selected_product.id)
          item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=int(selected_product.client_quantity),
            price=int(selected_product.price)
          )
          item_total = item.subtotal()
          order.total_amount += item_total
        order.save()
      except Exception as e:
        return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))
      return HttpResponse(json.dumps({"status": "success", "data": {"message": order_id}}))
    except Exception as e:
      return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))


  def find_total_amount(selected_products):
    for i in range(selected_products()):
      pass