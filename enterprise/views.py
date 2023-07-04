from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str
from paypal.standard.forms import PayPalPaymentsForm
import json
import base64
from decimal import Decimal
from datetime import datetime as dt
import datetime
from datetime import date
from django.db.models import Q, Sum
from django.core.paginator import Paginator


# Import models
from .models import Product, Order, OrderItem, ExpenseCategory, Expense, User, Loan, Account, ProductCategory, MonthlyData

# Import project app logic
from .add_product import SaveProduct
from .create_account import CreateClientAccount
from .create_order import CreateOrder
from .create_admin import CreateAdmin
from .create_staff import CreateStaffAccount
from .create_expense import CreateExpense
from .process_order import ProcessOrder


# Create your views here.
@login_required
def homeview(request):
    # return HttpResponse('index.html')
    user = request.user
    return render(request, 'index.html', {'user': user})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def track_finances(request):
    # Get current month and year
    today = date.today()
    month = today.month
    year = today.year

    # Calculate total expenses for the current month
    total_expenses = Expense.objects.filter(date__month=month).aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate total sales for the current month
    total_sales = Order.objects.filter(order_date__month=month).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0

    # Calculate profit/loss
    profit_loss = total_sales - total_expenses

    # Create or update MonthlyData for the current month
    monthly_data, _ = MonthlyData.objects.get_or_create(month=month, year=year)
    monthly_data.total_expenses = total_expenses
    monthly_data.total_sales = total_sales
    monthly_data.profit_loss = profit_loss
    monthly_data.save()

    # Retrieve historical monthly data
    historical_data = MonthlyData.objects.order_by('-year', '-month')[:12]

    context = {
        'current_month_data': monthly_data,
        'historical_data': historical_data,
    }

    return render(request, 'finances.html', context)


@login_required
def admin_dashboard(request):
    loans = Loan.objects.all()
    expenses = Expense.objects.all()

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


def product(request, p_code):
    product = get_object_or_404(Product, p_code=p_code)
    p_categories = product.categories.all()
    print(p_categories)
    return render(request, 'product.html', {'product': product, 'categories': p_categories})

@login_required
def add_product(request):
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        name = request.POST.get('product_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        brand = request.POST.get('brand')
        # category = request.POST.get('category')
        category_ids = request.POST.getlist('categories')

        SaveProduct.save_new_product(
            name, description, price, image, quantity, brand, category_ids)
        return redirect('products')

    return render(request, 'add_product.html', {'categories': categories})


@login_required
def add_product_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        context = SaveProduct.create_product_category(name=name)
        return render(request, 'add_product_category.html', {'errors': context})
    return render(request, 'add_product_category.html')

# @login_required

@csrf_exempt
def products(request):
    try:
        products = Product.objects.all()

        if request.method == 'POST':
            query = request.POST.get('query')
            products = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__icontains=query))
            paginator = Paginator(products, 12)
            page_number = request.GET.get('page')
            if page_number is None:
                page_number = 1
            page_obj = paginator.get_page(page_number)
            # return redirect(reverse('products'))
            return render(request, 'products.html', {'products': page_obj})
        else:
            products = Product.objects.all()
            paginator = Paginator(products, 12)
            page_number = request.GET.get('page')
            if page_number is None:
                page_number = 1
            page_obj = paginator.get_page(page_number)
            # print(page_obj)
            return render(request, 'products.html', {'products': page_obj})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def search_products(request):
    query = request.GET.get('query', '')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(brand__icontains=query))
    return render(request, 'products.html', {'results': results})


@login_required
def manage_products(request):
    products = Product.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=int(product_id))
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        if price is None:
            price = product.price
        elif quantity is None:
            quantity = product.quantity
        print(product.__dict__)
        SaveProduct.update_product_price_quantity(product, quantity, price)

    return render(request, 'manage_products.html', {'products': products})


@login_required
def update_product(request, p_code):
    product = get_object_or_404(Product, p_code=p_code)
    if request.method == 'POST':
        SaveProduct.update_product_full()
        return redirect('product', args=[product.p_code])
    return render(request, 'update_product.html', {'product': product})


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
            orders = Order.objects.filter(
                client=request.user, status='pending')
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
            orders = Order.objects.filter(
                client=request.user, status='completed')
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
        print(selected_products[0].__dict__)
        for i in range(len(products)):
            p_quantity = request.POST.get(str(selected_products[i]))
            quantity = request.POST.get(f'{selected_products[i]}-quantity')
            print(quantity)
            selected_products[i].client_quantity = quantity
        print(selected_products[0].__dict__)

        if payment_method is None:
            payment_method = 'paypal'
        total_amount = 0
        shipping_address = request.POST.get('shipping_address')
        CreateOrder.create_new_order(
            user, payment_method, total_amount, shipping_address, selected_products)

        return redirect('orders')

    return render(request, 'new_order.html', {'selected_products': selected_products})


def confirm_order(request):
    if request.method == 'POST':
        print(request.__dict__)
        return redirect('order')


def add_to_order(request):
    try:
        if request.method == 'POST':
            order_items = json.loads(request.POST.get('cart_items'))

        return render(request, 'order.html')
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


@login_required
def user(request, user_id):
    user = get_object_or_404(User, user_id=user_id)
    orders = Order.objects.filter(client=request.user)
    num_orders = len(orders)
    return render(request, 'user.html', {'user': user, 'num_orders': num_orders})


def system_users(request):
    try:
        users = list(User.objects.all())

        return render(request, 'users.html', {'users': users, 'u': 'Users'})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_admins(request):
    try:
        users = User.objects.filter(is_admin=True)

        return render(request, 'users.html', {'users': users, 'u': 'Admins'})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_clients(request):
    try:
        users = User.objects.filter(is_staff=False)

        return render(request, 'users.html', {'users': users, 'u': 'Clients'})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_staff(request):
    try:
        users = User.objects.filter(is_staff=True)
        # print(order_items)

        return render(request, 'users.html', {'users': users, 'u': 'Staff'})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def system_archived_users(request):
    try:
        users = User.objects.filter(is_archived=True)

        return render(request, 'users.html', {'users': users, 'u': 'Archived users'})
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
        # print(order_items)
        if request.method == 'POST':
            return redirect('process_payment')
        return render(request, 'order.html', {'order': order, 'order_items': order_items})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


def process_order(request, order_code):
    try:
        order = get_object_or_404(Order, order_code=order_code)
        if request.method == 'POST':
            status = request.POST.get('status')
            print(status)
            ProcessOrder.process_order(order, request.user, status)
        return render(request, 'process_order.html', {'order': order})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'fail', 'data': {'message': str(e)}}))


class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    def get_html_submit_element(self):
        return """<button type="submit">Continue on PayPal website</button>"""


def process_payment(request, order_code):
    try:
        order = get_object_or_404(Order, order_code=order_code)
        order_items = OrderItem.objects.filter(order_id=order.id)
        print(order_items)
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
        return render(request, 'process_payment.html', {'order': order, 'order_items': order_items, 'form': form})
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))


@csrf_exempt
def payment_done(request):
    return render(request, 'payment_done.html')


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment_cancelled.html')


def expenses(request):
    expenses = get_list_or_404(Expense)
    time = dt.now()
    month = time.strftime("%B %Y")
    date = datetime.date.today()

    return render(request, 'expenses.html', {'expenses': expenses, 'month': month})


def expense(request, e_code):
    expense = get_object_or_404(Expense, e_code=e_code)
    return render(request, 'expense.html', {'expense': expense})


def new_expense(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        category = request.POST.get('e_category')
        staff = request.user

        expense = CreateExpense.create_new_expense(
            user, description, amount, category, staff)
        print(expense.__dict__)

        return redirect(reverse('expense', kwargs={'e_code': expense.e_code}))

    expense_categories = ExpenseCategory.objects.all()

    return render(request, 'new_expense.html', {'expense_categories': expense_categories})


def expense_category(request):
    pass


@login_required
def profile(request):
    user = request.user
    name = user.first_name + user.last_name

    return render(request, 'profile.html', {'user': user, 'name': name})


def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user:
            # Generate the password reset token
            user_id = user.user_id
            # uid = base64.urlsafe_b64decode(uid.encode()).decode('latin-1')
            token = default_token_generator.make_token(user)

            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': user_id, 'token': token}))
            subject = 'Password Reset'
            message = f'Click the link below to reset your password:\n\n{reset_url}'
            send_mail(subject, message, 'itsmraga@gmail.com', [email])

            messages.success(
                request, 'Password reset instructions have been sent to your email.')
            return redirect('client_login')
        else:
            messages.error(request, 'Invalid email address.')

    return render(request, 'password_reset.html')


def password_reset_confirm(request, uidb64, token):
    try:
        user = User.objects.get(user_id=uidb64)
        # uidb64 = uidb64
        # token = token
        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                new_password1 = request.POST.get('new_password1')
                new_password2 = request.POST.get('new_password2')
                if new_password1 == new_password2:
                    user.set_password(new_password1)
                    user.save()
                    messages.success(
                        request, 'Your password has been reset successfully. You can now login.')
                    return redirect('client_login')
                else:
                    messages.error(request, 'Passwords do not match.')
            return render(request, 'password_reset_confirm.html', {'token': token, 'uidb64': uidb64})
        else:
            messages.error(request, 'Invalid reset link. Please try again.')
    # except (TypeError, ValueError, OverflowError, User.DoesNotExist):
    except Exception as e:
        return HttpResponse(json.dumps({'status': 'failed', 'data': {'message': str(e)}}))
        # messages.error(request, 'Invalid reset link. Please try again.'


def password_reset_done(request):
    return render(request, 'password_reset_done.html')
