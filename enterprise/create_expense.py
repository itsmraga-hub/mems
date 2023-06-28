from django.http import HttpResponse

import json
import uuid

from .models import Expense, ExpenseCategory


class CreateExpense:
  def __init__(self):
    pass

  def create_new_expense(user, description, amount, category, staff):
    try:
      e_c = ExpenseCategory.objects.get(ec_code=category)
      e_code = str(uuid.uuid4())
      expense = Expense.objects.create(
        e_code=e_code,
        description=description,
        staff=staff,
        amount=amount,
        category=e_c
      )
      return expense
      # return HttpResponse(json.dumps({"status": "success", "data": {"message": e_code}}))
    except Exception as e:
      return HttpResponse(json.dumps({"status": "fail", "data": {"message": str(e)}}))


  def find_total_amount(selected_products):
    for i in range(selected_products()):
      pass