from django.http import HttpResponse

import json
import uuid

from .models import Product

class SaveProduct:
  def __init__(self):
    pass

  def save_new_product(self, name, description, price, image, quantity, brand, category):
    try:
      p_code = str(uuid.uuid4())
      product = Product(
        p_code=p_code,
        name=name,
        description=description,
        price=price,
        image=image, 
        quantity=quantity,
        brand=brand,
        category=category
      )
      print(product)
      product.save()
      return HttpResponse(json.dumps({"status": "success", "data": {"message": p_code}}))
    except Exception as e:
      return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))

  def update_product(product, quantity, price):
    product.quantity = quantity
    product.price = price
    product.save()

  def update_product_full(product):
    pass