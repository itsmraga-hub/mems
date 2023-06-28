from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
import json


# Import models
from .models import Product, Order, OrderItem, ExpenseCategory, Expense, User, Loan, Account

# Import project app logic
from .add_product import SaveProduct
from .create_account import CreateClientAccount
from .create_order import CreateOrder
from .create_admin import CreateAdmin
from .create_staff import CreateStaffAccount
from .create_expense import CreateExpense


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
                res = CreateClientAccount.save_client_account(
                    '', first_name, last_name, email, phone, password1)
                auth_user = authenticate(
                    request, email=email, password=password1)
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

        SaveProduct.save_new_product(
            '', name, description, price, image, quantity, brand, category)
        return redirect('products')

    return render(request, 'add_product.html')


# @login_required
def products(request):
    try:
        products = Product.objects.all()
        return render(request, 'products.html', {'products': products})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


@login_required
def orders(request):
    try:
        orders = []
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(client=request.user)
        
        return render(request, 'orders.html', {'orders': orders})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


@login_required
def pending_orders(request):
    try:
        # orders = Order.objects.filter(status='pending')
        orders = []
        if request.user.is_staff:
            orders = Order.objects.filter(status='pending')
        else:
            orders = Order.objects.filter(client=request.user, status='pending')
        return render(request, 'orders.html', {'orders': orders})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


@login_required
def completed_orders(request):
    try:
        # orders = Order.objects.filter(status='completed')
        orders = []
        if request.user.is_staff:
            orders = Order.objects.filter(status='completed')
        else:
            orders = Order.objects.filter(client=request.user, status='completed')
        return render(request, 'orders.html', {'orders': orders})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


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
        CreateOrder.create_new_order(
            user, payment_method, total_amount, shipping_address, selected_products)

        return redirect('orders')

    return render(request, 'new_order.html', {'selected_products': selected_products})


def confirm_order(request):
    if request.method == 'POST':
        # order = Order.objects.create()
        print(request.__dict__)
        return redirect('order')


def add_to_order(request):
    try:
        if request.method == 'POST':
            order_items = json.loads(request.POST.get('cart_items'))
            # print(order_items)

        return render(request, 'order.html')
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def user(request, user_id):
    user = User.objects.get(user_id=user_id)
    return render(request, 'user.html', {'user': user})


def system_users(request):
    try:
        users = list(User.objects.all())

        return render(request, 'users.html', {'users': users})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_admins(request):
    try:
        users = User.objects.filter(is_admin=True)
        # print(order_items)

        return render(request, 'users.html', {'users': users})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_clients(request):
    try:
        users = User.objects.filter(is_staff=False)
        # print(order_items)

        return render(request, 'users.html', {'users': users})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_staff(request):
    try:
        users = User.objects.filter(is_staff=True)
        # print(order_items)

        return render(request, 'users.html', {'users': users})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_archived_users(request):
    try:
        users = User.objects.filter(is_archived=True)
        # print(order_items)

        return render(request, 'users.html', {'users': users})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def create_admin(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            phone = request.POST.get('phone')
            if password1 == password2:
                CreateAdmin.save_admin_account(
                    '', first_name, last_name, email, phone, password1)

                return redirect('dashboard')
            else:
                return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': 'Password didn\'t match. Check and try again!'}}))
        else:
            return render(request, 'add_admin.html')
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))


def create_staff(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            phone = request.POST.get('phone')
            if password1 == password2:
                CreateStaffAccount.save_staff_account(
                    '', first_name, last_name, email, phone, password1)

                return redirect('dashboard')
            else:
                return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': 'Password didn\'t match. Check and try again!'}}))
        else:
            # return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': 'Try again after some time'}}))
            return render(request, 'staff_signup.html')
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))


def order(request, order_code):
    try:
        order = Order.objects.get(order_code=order_code)
        order_items = OrderItem.objects.filter(order_id=order.id)
        if request.method == 'POST':
          return redirect('process_payment')
        return render(request, 'order.html', {'order': order, 'order_items': order_items})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


class CustomPayPalPaymentsForm(PayPalPaymentsForm):
  def get_html_submit_element(self):
    return """<button type="submit">Continue on PayPal website</button>"""


def process_payment(request, order_code):
  try:
    order = get_object_or_404(Order, order_code=order_code)
    # host = request.get_host()
    order.total_amount = order.total_cost()
    order.save()

    paypal_dict = {
      'business': settings.PAYPAL_RECEIVER_EMAIL,
      'amount': '%.2f' % order.total_amount,
      'item_name': 'Order {}'.format(order.order_code),
      'invoice': str(order.order_code),
      'currency_code': 'USD',
      "item_name": "Order #{}".format(order.id),
      "invoice": "unique-invoice-id",
      "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
      "return": request.build_absolute_uri(reverse('payment_done')),
      "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
      "custom": "{}".format(order.order_code),
      "invoice": "{}".format(order.order_code)
    }
    form = CustomPayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'order': order, 'form': form})
  except Exception as e:
    return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))

@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')


def expenses(request):
    try:
        expenses = Expense.objects.all()
        return render(request, 'expenses.html', {'expenses': expenses})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))


def expense(request, e_code):
    expense = get_object_or_404(Expense, e_code=e_code)
    return render(request, 'expense.html', {'expense': expense})

def new_expense(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('e_category')
        staff = request.user

        expense = CreateExpense.create_new_expense(user, description, amount, category, staff)
        print(expense.__dict__)

        return redirect(reverse('expense', kwargs={'e_code': expense.e_code}))

    expense_categories = ExpenseCategory.objects.all()

    return render(request, 'new_expense.html', {'expense_categories': expense_categories})



def expense_category(request):
    pass