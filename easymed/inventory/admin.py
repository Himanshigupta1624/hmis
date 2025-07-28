from django.contrib import admin
from .models import Category, Supplier, Item, StockTransaction, PurchaseOrder, PurchaseOrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'phone', 'email']
    search_fields = ['name', 'contact_person', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'category', 'current_stock', 'minimum_stock', 'unit_price', 'is_low_stock']
    list_filter = ['category', 'supplier', 'is_active', 'unit']
    search_fields = ['name', 'sku', 'barcode']
    readonly_fields = ['created_at', 'updated_at', 'stock_value']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'sku', 'unit')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'stock_value')
        }),
        ('Stock Information', {
            'fields': ('current_stock', 'minimum_stock', 'maximum_stock')
        }),
        ('Supplier & Location', {
            'fields': ('supplier', 'storage_location')
        }),
        ('Additional', {
            'fields': ('barcode', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_type', 'quantity', 'unit_price', 'total_price', 'created_by', 'created_at']
    list_filter = ['transaction_type', 'created_at']
    search_fields = ['item__name', 'reference_number']
    readonly_fields = ['total_price', 'created_at']


class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1
    readonly_fields = ['total_price']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier', 'order_date', 'status', 'total_amount']
    list_filter = ['status', 'order_date']
    search_fields = ['order_number', 'supplier__name']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [PurchaseOrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'supplier', 'order_date', 'expected_delivery_date', 'status')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Additional', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at')
        }),
    )
