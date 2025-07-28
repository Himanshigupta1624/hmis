from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db import models
from datetime import datetime
from .models import Announcement, AnnouncementRead
from .serializers import AnnouncementSerializer, AnnouncementListSerializer
from django.shortcuts import render


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def announcement_list(request):
    if request.method == 'GET':
        announcements = Announcement.objects.filter(is_active=True)
        
        # Filter by audience
        user_role = request.user.role
        announcements = announcements.filter(
            audience__in=['all', user_role]
        )
        
        # Filter by current announcements
        current_only = request.GET.get('current')
        if current_only == 'true':
            now = datetime.now()
            announcements = announcements.filter(
                start_date__lte=now
            ).filter(
                models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
            )
        
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(announcements, request)
        serializer = AnnouncementListSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    elif request.method == 'POST':
        # Only admin can create announcements
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AnnouncementSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def announcement_detail(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == 'GET':
        serializer = AnnouncementSerializer(announcement, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if request.user.role != 'admin':
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_as_read(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    
    # Create or get the read record
    read_record, created = AnnouncementRead.objects.get_or_create(
        announcement=announcement,
        user=request.user
    )
    
    return Response({'message': 'Announcement marked as read'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_announcements(request):
    # Get announcements that the user hasn't read
    read_announcement_ids = AnnouncementRead.objects.filter(
        user=request.user
    ).values_list('announcement_id', flat=True)
    
    announcements = Announcement.objects.filter(
        is_active=True
    ).exclude(
        id__in=read_announcement_ids
    ).filter(
        audience__in=['all', request.user.role]
    )
    
    # Filter current announcements
    now = datetime.now()
    announcements = announcements.filter(
        start_date__lte=now
    ).filter(
        models.Q(end_date__isnull=True) | models.Q(end_date__gte=now)
    )
    
    serializer = AnnouncementListSerializer(announcements, many=True, context={'request': request})
    return Response(serializer.data)

# Create your views here.
