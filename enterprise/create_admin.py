from django.http import HttpResponse
import json
import uuid
from .models import User


class CreateAdmin:
  def __init__(self):
    pass

  def save_admin_account(self, first_name, last_name, email, phone, password1):
    try:
      email = email.strip()
      email = email.replace(' ', '')
      u_id = str(uuid.uuid4())
      user_exists = User.objects.filter(email=email).exists()
      if user_exists:
        data = {"status": "fail", "data": {"message": "User already exists"}}
        return HttpResponse(json.dumps(data), content_type='text/json')
      user = User(
        first_name=first_name,
        last_name=last_name,
        username=email,
        user_id=u_id,
        email=email,
        phone=phone,
        is_admin=True,
        is_staff=True
      )
      user.set_password(password1)
      user.save()
      return HttpResponse(json.dumps({'status': 'success', 'data': {'message': str(u_id)}, 'user': str(user)}))
    except Exception as e:
      return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))