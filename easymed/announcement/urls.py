from django.urls import path
from . import views

urlpatterns = [
    path('', views.announcement_list, name='announcement-list'),
    path('<int:pk>/', views.announcement_detail, name='announcement-detail'),
    path('<int:pk>/mark-read/', views.mark_as_read, name='mark-announcement-read'),
    path('unread/', views.unread_announcements, name='unread-announcements'),
]