from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Invoice, InvoiceItem, Payment, InsuranceClaim
from .serializers import InvoiceSerializer, InvoiceListSerializer, PaymentSerializer, InsuranceClaimSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def invoice_list(request):
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        status_filter = request.GET.get('status')
        patient_id = request.GET.get('patient')
        
        if status_filter:
            invoices = invoices.filter(status=status_filter)
        if patient_id:
            invoices = invoices.filter(patient_id=patient_id)
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(invoices, request)
        serializer = InvoiceListSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = InvoiceSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'GET':
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InvoiceSerializer(invoice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    data = request.data.copy()
    data['invoice'] = invoice.id
    data['received_by'] = request.user.id
    
    serializer = PaymentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def insurance_claim_list(request):
    if request.method == 'GET':
        claims = InsuranceClaim.objects.all()
        status_filter = request.GET.get('status')
        if status_filter:
            claims = claims.filter(status=status_filter)
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(claims, request)
        serializer = InsuranceClaimSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        serializer = InsuranceClaimSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def overdue_invoices(request):
    invoices = Invoice.objects.all()
    overdue_invoices = [invoice for invoice in invoices if invoice.is_overdue]
    serializer = InvoiceListSerializer(overdue_invoices, many=True)
    return Response(serializer.data)
