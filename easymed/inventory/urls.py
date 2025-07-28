from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.category_list, name='category-list'),
    path('suppliers/', views.supplier_list, name='supplier-list'),
    path('items/', views.item_list, name='item-list'),
    path('items/<int:pk>/', views.item_detail, name='item-detail'),
    path('items/low-stock/', views.low_stock_items, name='low-stock-items'),
    path('transactions/', views.stock_transaction_list, name='stock-transaction-list'),
    path('purchase-orders/', views.purchase_order_list, name='purchase-order-list'),
]