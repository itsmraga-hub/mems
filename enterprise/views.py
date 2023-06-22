from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from .models import Product
from .add_product import SaveProduct


# Create your views here.
def homeview(request):
  # return HttpResponse('index.html')
  return render(request, 'index.html')


def dashboard(request):
  return render(request, 'dashboard.html')


def admin_dashboard(request):
  return render(request, 'admin_dashboard.html')

def client_signup(request):
  if request.method == 'POST':
    email = request.POST.get('email')

    return redirect('dashboard')

def client_login(request):
  if request.method == 'POST':
    email = request.POST.get('email')



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

def products(request):
  try:
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))