from django.contrib import admin
from .models import Medicine, Prescription, PrescriptionItem


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'strength', 'form', 'manufacturer', 'stock_quantity', 'price_per_unit', 'expiry_date']
    list_filter = ['form', 'category', 'manufacturer', 'expiry_date']
    search_fields = ['name', 'generic_name', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at', 'total_value']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'generic_name', 'manufacturer', 'strength', 'form', 'category')
        }),
        ('Stock Information', {
            'fields': ('stock_quantity', 'reorder_level', 'price_per_unit', 'total_value')
        }),
        ('Product Details', {
            'fields': ('description', 'expiry_date', 'batch_number', 'barcode')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1
    readonly_fields = ['unit_price', 'total_price']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'prescription_date', 'status', 'total_amount']
    list_filter = ['status', 'prescription_date', 'doctor']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [PrescriptionItemInline]
    
    fieldsets = (
        ('Prescription Details', {
            'fields': ('patient', 'doctor', 'prescription_date', 'status')
        }),
        ('Dispensing Information', {
            'fields': ('dispensed_by', 'dispensed_at', 'total_amount')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_at', 'updated_at')
        }),
    )