from django.urls import path
from . import views

urlpatterns = [
    path('invoices/', views.invoice_list, name='invoice-list'),
    path('invoices/<int:pk>/', views.invoice_detail, name='invoice-detail'),
    path('invoices/<int:invoice_id>/payments/', views.add_payment, name='add-payment'),
    path('invoices/overdue/', views.overdue_invoices, name='overdue-invoices'),
    path('insurance-claims/', views.insurance_claim_list, name='insurance-claim-list'),
]