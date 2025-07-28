from rest_framework import serializers
from .models import Paitent,PaitentVisit

class PaitentSerializer(serializers.ModelSerializer):
    age=serializers.ReadOnlyField()
    full_name=serializers.ReadOnlyField()
    
    class Meta:
        model=Paitent
        fields='__all__'
        read_only_fields=['created_by','created_at','updated_at']
    
    def create(self,validated_data):
        validated_data['created_by']=self.context['request'].user
        return super().create(validated_data)

class PaitentVisitSerializer(serializers.ModelSerializer):
    paitent_name=serializers.CharField(source='paitent.full_name',read_only=True)
    doctor_name=serializers.CharField(source='doctor.full_name',read_only=True)  
    
    class Meta:
        model=PaitentVisit
        fields='__all__'
        read_only_fields=['created_at','updated_at']


class PaitentListSerializer(serializers.ModelSerializer):
    age=serializers.ReadOnlyField()
    full_name=serializers.ReadOnlyField()
    class Meta:
        model=Paitent
        fields=['id', 'patient_id', 'full_name', 'age', 'gender', 'phone', 'created_at']            