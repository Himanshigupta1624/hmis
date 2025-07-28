from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """Custom user model with email as username field"""
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone=models.CharField(max_length=15,blank=True)
    address=models.TextField(blank=True)
    date_of_birth=models.DateField(null=True,blank=True)
    profile_picture=models.ImageField(upload_to='profile_pics/',blank=True,null=True)
    
    ROLE_CHOICES=[
        ('admin','Admin'),
        ('doctor','Docter'),
        ('nurse','Nurse'),
        ('pharmacist','Pharmacist'),
        ('lab_technician','Lab Technician'),
        ('receptionist','Receptionist'),
    ]
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name']
    
    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name ({self.email})}"
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
