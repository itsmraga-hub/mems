from django.http import HttpResponse

import json
import uuid


from .models import Order


class ProcessOrder:
  def __init__(self):
    pass

  def process_order(order, user, status):
    try:
      order.staff = user
      order.status = status
      order.save()
      # print(order.__dict__)

      return HttpResponse(json.dumps({"status": "success", "data": {"message": "order processed"}}))
    except Exception as e:
      return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))
