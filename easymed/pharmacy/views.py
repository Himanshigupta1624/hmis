from rest_framework import status,permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Medicine,Prescription,PrescriptionItem
from .serializers import MedicineSerializer,PrescriptionSerializer,PrescriptionListSerializer


class StandardResultSetPagination(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=100

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def medicine_list(request):
    if request.method=='GET':
        medicines=Medicine.objects.all()
        search=request.GET.get('search')
        if search:
            medicines=medicines.filter(name__icontains=search)
        paginator=StandardResultSetPagination()
        page=paginator.paginate_queryset(medicines,request)   
        serializer=MedicineSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method=='POST':
        serializer=MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def medicine_detail(request,pk):
    medicine=get_object_or_404(Medicine,pk=pk)
    if request.method=='GET':
        serializer=MedicineSerializer(medicine)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=MedicineSerializer(medicine,data=request.data,partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  
    elif request.method=='DELETE':
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])   
def prescription_list(request):
    if request.method=='GET':
        prescriptions=Prescription.objects.all()
        status_filter=request.GET.get('status')     
        if status_filter:
            prescriptions=prescriptions.filter(status=status_filter)
        paginator=StandardResultSetPagination()
        page=paginator.paginate_queryset(prescriptions,request)
        serializer=PrescriptionListSerializer(page,many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method=='POST':
        serializer=MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def prescription_detail(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk)
    
    if request.method == 'GET':
        serializer = PrescriptionSerializer(prescription)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def low_stock_medicines(request) :
    medicines=Medicine.objects.filter(stock_quantity__lte=models.F('reorder_level'))
    serializer=MedicineSerializer(medicines,many=True)
    return Response(serializer.data)   
                

