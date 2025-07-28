from rest_framework import status,permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import LabTest,LabOrder,LabOrderItem,LabResult
from .serializers import LabTestSerializer,LabOrderSerializer,LabOrderListSerializer,LabOrderItemSerializer,LabResultSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=100
    
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])    
def lab_test_list(request):
    if request.method=='GET':
        tests=LabTest.objects.all()
        search=request.GET.get('search')
        if search:
            tests=tests.filter(name__icontains=search)
        paginator=StandardResultsSetPagination()
        page=paginator.paginate_queryset(tests,request)
        serializer=LabTestSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)    
    elif request.method=='POST':
        serializer=LabTestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def lab_test_detail(request,pk):
    test=get_object_or_404(LabTest,pk=pk)
    
    if request.method=='GET':
        serializer=LabTestSerializer(test)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=LabTestSerializer(test,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def lab_order_list(request):
    if request.method=='GET':
        orders=LabOrder.objects.all()
        status_filter=request.GET.get('status')
        if status_filter:
            orders=orders.filter(status=status_filter)
        
        paginator=StandardResultsSetPagination()
        page=paginator.paginate_queryset(orders,request)
        serializer=LabOrderListSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method=='POST':
        serializer=LabOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)  
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def lab_order_detail(request, pk):
    order = get_object_or_404(LabOrder, pk=pk)
    
    if request.method == 'GET':
        serializer = LabOrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = LabOrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_lab_result(request,order_item_id) :
    order_item = get_object_or_404(LabOrderItem, pk=order_item_id)
    data = request.data.copy()
    data['order_item'] = order_item.id
    
    serializer = LabResultSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             
