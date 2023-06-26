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
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('products/new', views.add_product, name='add_product'),
    path('products', views.products, name='products'),
    path('orders', views.orders, name='orders'),
    path('orders/pending', views.pending_orders, name='pending_orders'),
    path('orders/completed', views.completed_orders, name='completed_orders'),
    path('add_to_order', views.add_to_order, name='add_to_order'),
    path('orders/<str:order_code>', views.order, name='cart_order'),
    path('order/', views.new_order, name='new_order'),
    path('confirm-order', views.confirm_order, name='confirm_order')
    # path()
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
