from django.contrib import admin
from .models import Invoice, InvoiceItem, Payment, InsuranceClaim


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ['total_price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'patient', 'invoice_date', 'status', 'total_amount', 'paid_amount', 'balance_due']
    list_filter = ['status', 'invoice_date', 'created_at']
    search_fields = ['invoice_number', 'patient__first_name', 'patient__last_name']
    readonly_fields = ['subtotal', 'tax_amount', 'total_amount', 'balance_due', 'created_at', 'updated_at']
    inlines = [InvoiceItemInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': ('invoice_number', 'patient', 'invoice_date', 'due_date', 'status')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax_rate', 'tax_amount', 'discount_amount', 'total_amount', 'paid_amount', 'balance_due')
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at')
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['invoice', 'payment_date', 'amount', 'payment_method', 'received_by']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['invoice__invoice_number', 'reference_number']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('invoice', 'payment_date', 'amount', 'payment_method')
        }),
        ('Details', {
            'fields': ('reference_number', 'notes', 'received_by')
        }),
        ('System Information', {
            'fields': ('created_at',)
        }),
    )


@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_number', 'patient', 'insurance_company', 'claim_amount', 'approved_amount', 'status']
    list_filter = ['status', 'submission_date', 'insurance_company']
    search_fields = ['claim_number', 'patient__first_name', 'patient__last_name', 'policy_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Claim Information', {
            'fields': ('claim_number', 'patient', 'invoice', 'submission_date', 'status')
        }),
        ('Insurance Details', {
            'fields': ('insurance_company', 'policy_number', 'claim_amount', 'approved_amount')
        }),
        ('Dates', {
            'fields': ('response_date',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at')
        }),
    )
