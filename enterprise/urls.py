# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.homeview, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('clients/signup', views.client_signup, name='client_signup'),
    path('clients/login', views.client_login, name='client_login'),
    path('signout', LogoutView.as_view(), name='signout'),
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('products/new', views.add_product, name='add_product'),
    path('product_category/new', views.add_product_category, name='add_product_category'),
    path('products', views.products, name='products'),
    path('product/<str:p_code>', views.product, name='product'),
    path('products/search/', views.search_products, name='search'),
    path('manage-products', views.manage_products, name='manage_products'),
    path('product-update/<str:p_code>', views.update_product, name='update_product'),
    path('orders', views.orders, name='orders'),
    path('my_orders', views.my_orders, name='my_orders'),
    path('finances', views.track_finances, name='finances'),
    path('orders/pending', views.pending_orders, name='pending_orders'),
    path('orders/completed', views.completed_orders, name='completed_orders'),
    path('orders/cancelled', views.cancelled_orders, name='cancelled_orders'),
    path('add_to_order', views.add_to_order, name='add_to_order'),
    path('orders/<str:order_code>', views.order, name='order'),
    path('order/', views.new_order, name='new_order'),
    path('order/process/<str:order_code>', views.process_order, name='process_order'),
    path('confirm-order', views.confirm_order, name='confirm_order'),
    path('users', views.system_users, name='users'),
    path('admins', views.system_admins, name='admins'),
    path('user/<str:user_id>', views.user, name='user'),
    path('staff', views.system_staff, name='staff'),
    path('clients', views.system_clients, name='clients'),
    path('archived-users', views.system_archived_users, name='archived_users'),
    path('create-admin', views.create_admin, name='create_admin'),
    path('create-staff', views.create_staff, name='create_staff'),
    path('process-payment/<str:order_code>', views.process_payment, name='process_payment'),
    path('payment-done', views.payment_done, name='payment_done'),
    path('payment-cancelled', views.payment_cancelled, name='payment_cancelled'),
    path('expenses/', views.expenses, name='expenses'),
    path('new_expense', views.new_expense, name='new_expense'),
    path('expenses/<str:e_code>', views.expense, name='expense'),
    path('profile', views.profile, name='profile'),
    path('password-reset/', views.password_reset, name='password_reset'),
    path('password-reset/done/', views.password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<str:uidb64>/<str:token>', views.password_reset_confirm, name='password_reset_confirm'),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
