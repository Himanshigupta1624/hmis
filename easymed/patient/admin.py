from django.contrib import admin
from .models import Patient,PatientVisit

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display=['patient_id','first_name','last_name','gender','blood_group','phone','created_at']
    list_filter=['gender','blood_group','created_at']
    search_fields=['patient_id','first_name','last_name','phone','email']
    readonly_fields=['created_at','updated_at']
    
    fieldsets=(
        ('Personal Information',{
            'fields':('paitent_id','first_name','last_name','date_of_birth','gender','blood_group')
        }),
        ('Contact Information',{
            'fields':( 'phone','email','address')
        }),
        ('Emergency Contact',{
            'fields':('emergency_contact_name','emergency_contact_phone')
        }),
        ('Medical Information',{
            'fields':('medical_history','allergies')
        }),
        ('System Information',{
            'fields':('created_by','created_at','updated_at')
        }),
    )

@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display=['patient','visit_date','doctor','created_at']
    list_filter=['visit_date', 'doctor', 'created_at']    
    search_fields = ['patient__first_name', 'patient__last_name', 'patient__patient_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('patient', 'visit_date', 'doctor')
        }),
        ('Medical Details', {
            'fields': ('symptoms', 'diagnosis', 'treatment', 'notes')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )