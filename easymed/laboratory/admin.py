from django.contrib import admin
from .models import LabTest, LabOrder, LabOrderItem, LabResult


@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'unit', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'category']
    readonly_fields = ['created_at', 'updated_at']


class LabOrderItemInline(admin.TabularInline):
    model = LabOrderItem
    extra = 1
    readonly_fields = ['unit_prices', 'total_prices']


@admin.register(LabOrder)
class LabOrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'patient', 'doctor', 'order_date', 'status', 'priority', 'total_amount']
    list_filter = ['status', 'priority', 'order_date']
    search_fields = ['order_id', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [LabOrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'patient', 'doctor', 'order_date', 'status', 'priority')
        }),
        ('Collection Information', {
            'fields': ('collected_by', 'collected_at', 'completed_at')
        }),
        ('Additional Information', {
            'fields': ('notes', 'total_amount', 'created_at', 'updated_at')
        }),
    )


@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ['order_item', 'is_normal', 'tested_by', 'tested_at', 'verified_by']
    list_filter = ['is_normal', 'tested_at', 'verified_at']
    search_fields = ['order_item__test__name', 'order_item__order__patient__first_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Result Information', {
            'fields': ('order_item', 'result_value', 'is_normal', 'comments')
        }),
        ('Testing Information', {
            'fields': ('tested_by', 'tested_at', 'verified_by', 'verified_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
