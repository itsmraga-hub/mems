from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import json

# Import models
from .models import Product, Order, OrderItem, ExpenseCategory, Expense

# Import project app logic
from .add_product import SaveProduct
from.create_account import CreateClientAccount
from.create_order import CreateOrder



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

  
def orders(request):
  try:
    orders = Order.objects.all()
    return render(request, 'orders.html', {'orders': orders})
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))
  

def pending_orders(request):
  try:
    orders = Order.objects.filter(status='pending')
    return render(request, 'orders.html', {'orders': orders})
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def completed_orders(request):
  try:
    orders = Order.objects.filter(status='completed')
    return render(request, 'orders.html', {'orders': orders})
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def order(request, order_code):
  pass


@login_required
def new_order(request):
    products_param = request.GET.get('products')
    products = json.loads(products_param) if products_param else []
    # print(products)
    selected_products = []

    for i in range(len(products)):
      p_id = products[i].get('product_id')
      p = Product.objects.get(p_code=p_id)
      p.client_quantity = products[i].get('quantity', 1)
      selected_products.append(p)

    if request.method == 'POST':
      user = request.user
      payment_method = request.POST.get('payment_method')
      total_amount = 0
      shipping_address = request.POST.get('shipping_address')
      CreateOrder.create_new_order(user, payment_method, total_amount, shipping_address, selected_products)

      return redirect('orders')

    return render(request, 'new_order.html', {'selected_products': selected_products})


def confirm_order(request):
  if request.method == 'POST':
    # order = Order.objects.create()
    print(request.__dict__)
    return redirect('cart_order')


def add_to_order(request):
  try:
    if request.method == 'POST':
      order_items = json.loads(request.POST.get('cart_items'))
      # print(order_items)

    return render(request, 'order.html')
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))