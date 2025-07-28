from django.shortcuts import render
from rest_framework import status,permissions
from rest_framework.decorators import permission_classes,api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import Paitent,PaitentVisit
from .serializers import PaitentSerializer,PaitentListSerializer,PaitentVisitSerializer

class StandardResultsSetPagination(PageNumberPagination):
    page_size=10
    page_size_query_param='page_size'
    max_page_size=100
    
@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated]) 
def paitent_list(request):
    if request.method=='GET':
        paitents=Paitent.objects.all()
        search=request.GET.get('search')
        if search:
            paitents=paitents.filter(
                first_name__icontains=search
            )  | paitents.filter(
                last_name__icontains=search
            )| paitents.filter(
                paitent_id__icontains=search
            )
        
        paginator=StandardResultsSetPagination()
        page=paginator.paginate_queryset(paitents,request)
        serializer=PaitentListSerializer(page,many=True)    
        return paginator.get_paginated_response(serializer.data)
    elif request.method=='POST':
        serializer=PaitentSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([permissions.IsAuthenticated])
def paitent_detail(request,pk):
    paitent=get_object_or_404(Paitent,pk=pk)
    if request.method=='GET':
        serializer=PaitentSerializer(paitent)
        return Response(serializer.data)
    elif request.method=='PUT':
        serializer=PaitentSerializer(paitent,data=request.data,partial=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        paitent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
@permission_classes([permissions.IsAuthenticated])
def paitent_visits(request,paitent_id):
    paitent=get_object_or_404(Paitent,pk=paitent_id)
    if request.method=='GET':
        visits=PaitentVisit.objects.filter(paitent=paitent)
        serializer=PaitentVisitSerializer(visits,many=True)    
        return Response(serializer.data)
    elif request.method=='POST':
        data=request.data.copy()
        data['paitent']=paitent_id
        serializer=PaitentVisitSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
