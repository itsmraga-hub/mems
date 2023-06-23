from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# Import models
from .models import Product

# Import project app logic
from .add_product import SaveProduct
from.create_account import CreateClientAccount



# Create your views here.
def homeview(request):
  # return HttpResponse('index.html')
  return render(request, 'index.html')

@login_required
def dashboard(request):
  return render(request, 'dashboard.html')

@login_required
def admin_dashboard(request):
  return render(request, 'admin_dashboard.html')


def client_signup(request):
  try:
    if request.method == 'POST':
      email = request.POST.get('email')
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      password1 = request.POST.get('password1')
      password2 = request.POST.get('password2')
      phone = request.POST.get('phone')
      if password1 == password2:
        res = CreateClientAccount.save_client_account('', first_name, last_name, email, phone, password1)
        auth_user = authenticate(request, email=email, password=password1)
        login(request, auth_user)
        
        return redirect('dashboard')
      else:
        return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': 'Password didn\'t match. Check and try again!'}}))

      # return redirect('client_login')
    else:
      # return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': 'Try again after some time'}}))
      return render(request, 'client_signup.html')
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))


def client_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': 'failed to login'}}))

  return render(request, 'login.html')


@login_required
def add_product(request):
  if request.method == 'POST':
    name = request.POST.get('product_name')
    description = request.POST.get('description')
    price = request.POST.get('price')
    quantity = request.POST.get('quantity')
    image = request.FILES.get('image')
    brand = request.POST.get('brand')
    category = request.POST.get('category')

    SaveProduct.save_new_product('', name, description, price, image, quantity, brand, category)
    return redirect('products')

  return render(request, 'add_product.html')


# @login_required
def products(request):
  try:
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))