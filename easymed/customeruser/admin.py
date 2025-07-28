from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomeUserAdmin(UserAdmin):
    model=CustomUser
    list_display=['email','first_name','last_name','role','is_active','created_at']
    list_filter=['role','is_active','created_at']
    search_fields=['email','first_name','last_name']
    ordering=['email']
    
    fieldsets=UserAdmin.fieldsets +(
        (
            'Additional Info',{
                'fields':('phone','address','date_of_birth','profile_picture','role')
            }
        ),
    )
    add_fieldsets=UserAdmin.add_fieldsets+(
        ('Additional Info',{
            'fields':('email','first_name','last_name','phone','role')
        }),
    )
admin.site.register( CustomUser,CustomeUserAdmin)    