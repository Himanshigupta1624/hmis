from django.urls import path
from . import views

urlpatterns = [
    path('medicines/', views.medicine_list, name='medicine-list'),
    path('medicines/<int:pk>/', views.medicine_detail, name='medicine-detail'),
    path('medicines/low-stock/', views.low_stock_medicines, name='low-stock-medicines'),
    path('prescriptions/', views.prescription_list, name='prescription-list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription-detail'),
]