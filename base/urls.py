from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('load_invoice/', views.loadInvoice , name='load-invoice'),
    path('get_invoice_status/<str:invoiceNumber>/', views.getInvoiceStatus , name='get-invoice'),
    path('update_invoice/<str:invoiceNumber>/', views.updateInvoice , name='get-invoice'),
]