from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_create'),
    path('clients/<int:pk>/edit/', views.client_update, name='client_update'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/add/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('invoices/<int:invoice_id>/items/add/', views.item_create, name='item_create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name="register"),
    path("invoices/<int:pk>/edit/", views.invoice_update, name="invoice_update"),
    path("invoices/<int:pk>/delete/", views.invoice_delete, name="invoice_delete"),
    path("items/<int:pk>/edit/", views.item_update, name="item_update"),
    path("items/<int:pk>/delete/", views.item_delete, name="item_delete"),
    path("invoices/<int:pk>/pdf/", views.invoice_pdf, name="invoice_pdf"),
    path("api/clients/", views.api_clients),
    path("api/invoices/", views.api_invoices),

]
