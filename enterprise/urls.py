# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.homeview, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('clients/signup', views.client_signup, name='client_signup'),
    path('clients/login', views.client_login, name='client_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/new', views.add_product, name='add_product'),
    path('products', views.products, name='products')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
