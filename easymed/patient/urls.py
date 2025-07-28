from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient-list'),
    path('<int:pk>/', views.patient_detail, name='patient-detail'),
    path('<int:patient_id>/visits/', views.patient_visits, name='patient-visits'),
]