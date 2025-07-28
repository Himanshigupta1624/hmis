from rest_framework import status,permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Category,Supplier,Item,StockTransaction,PurchaseOrder
from .serializers import (
    CategorySerializer,SupplierSerializer,ItemSerializer,ItemListSerializer,
    StockTransactionSerializer,PurchaseOrderSerializer,PurchaseOrderListSerializer,PurchaseOrderItemSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=100

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def category_list(request):
    if request.method=='GET':
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)   
        return Response(serializer.data)
    elif request.method=='POST':
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def supplier_list(request):
    if request.method=='GET':
        suppliers=Supplier.objects.all()
        serializers=SupplierSerializer(suppliers,many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def item_list(request):
    if request.method=='GET':
        items=Item.objects.filter(is_active=True)
        search=request.GET.get('search')   
        category=request.GET.get('category')
        low_stock=request.GET.get('low_stock')
        
        if search:
            items=items.filter(name__icontains=search)
        if category:
            items=items.filter(category_id=category)
        if low_stock=='true':
            items=[item for item in items if item.is_low_stock]  
        
        paginator=StandardResultsSetPagination()
        page=paginator.paginate_queryset(items,request)
        serializer=ItemListSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method=='POST':
        serializer=ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED) 
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def item_detail(request,pk):
    item=get_object_or_404(Item,pk=pk)
    if request.method=='GET':
        serializer=ItemSerializer(item)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        item.is_active = False
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def stock_transaction_list(request):
    if request.method=='GET':
        transactions=StockTransaction.objects.all()
        item_id=request.GET.get('item')
        if item_id:
            transactions=transactions.filter(item_id=item_id)
        paginator=StandardResultsSetPagination()
        page=paginator.paginate_queryset(transactions,request)   
        serializer=StockTransactionSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)    
    elif request.method == 'POST':
        serializer = StockTransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def purchase_order_list(request):
    if request.method == 'GET':
        orders = PurchaseOrder.objects.all()
        status_filter = request.GET.get('status')
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(orders, request)
        serializer = PurchaseOrderListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def low_stock_items(request):
    items = Item.objects.filter(is_active=True)
    low_stock_items = [item for item in items if item.is_low_stock]
    serializer = ItemListSerializer(low_stock_items, many=True)
    return Response(serializer.data)    
    
    
        
              
        
