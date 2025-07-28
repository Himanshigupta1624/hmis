from rest_framework import serializers
from .models import Announcement, AnnouncementRead


class AnnouncementSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    is_current = serializers.ReadOnlyField()
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
    
    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AnnouncementRead.objects.filter(
                announcement=obj, 
                user=request.user
            ).exists()
        return False
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class AnnouncementListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True)
    is_current = serializers.ReadOnlyField()
    is_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'priority', 'audience', 'is_active', 'start_date', 'end_date', 
                 'created_by_name', 'created_at', 'is_current', 'is_read']
    
    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return AnnouncementRead.objects.filter(
                announcement=obj, 
                user=request.user
            ).exists()
        return False