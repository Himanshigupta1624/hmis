from rest_framework import serializers
from .models import LabTest,LabOrder,LabOrderItem,LabResult

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = '__all__'

class  LabResultSerializer(serializers.ModelSerializer):
    test_name=serializers.CharField(source='order_item.test.name',read_only=True)
    tested_by_name=serializers.CharField(source='tested_by.full_name',read_only=True)
    
    class Meta:
        model=LabResult
        fields='__all__'

class LabOrderItemSerializer(serializers.ModelSerializer):
    test_name=serializers.CharField(source='test.name',read_only=True)
    result=LabResultSerializer(read_only=True)
    
    class Meta:
        model=LabOrderItem
        fields='__all__'
        read_only_fields=['unit_price','toral_price']
        

class LabOrderSerializer(serializers.ModelSerializer):
    items=LabOrderItemSerializer(many=True,read_only=True)
    paitent_name=serializers.CharField(source='paitent.full_name',read_only=True)
    doctor_name=serializers.CharField(source='doctor.full_name',read_only=True)
    class Meta:
        model=LabOrder
        fields='__all__'
        read_only_fields=['total_amount','created_at','updated_at']

class LabOrderListSerializer(serializers.ModelSerializer):
    paitent_name=serializers.CharField(source='paitent.full_name',read_only=True)
    doctor_name=serializers.CharField(source='doctor.full_name', read_only=True)
    class Meta:
        model=LabOrder
        fields=['id', 'order_id', 'patient_name', 'doctor_name', 'order_date', 'status', 'priority', 'total_amount']  
              
                          