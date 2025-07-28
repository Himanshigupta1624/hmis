from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.lab_test_list, name='lab-test-list'),
    path('tests/<int:pk>/', views.lab_test_detail, name='lab-test-detail'),
    path('orders/', views.lab_order_list, name='lab-order-list'),
    path('orders/<int:pk>/', views.lab_order_detail, name='lab-order-detail'),
    path('results/<int:order_item_id>/', views.add_lab_result, name='add-lab-result'),
]