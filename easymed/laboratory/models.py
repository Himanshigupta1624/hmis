from django.db import models
from django.conf import settings
from patient.models import Patient


class LabTest(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    category=models.CharField(max_length=100)
    normal_range=models.CharField(max_length=200,blank=True)
    unit=models.CharField(max_length=50,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    preparation_required=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['name']
    
    def __str__(self):
            return self.name


class LabOrder(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('collected','Sample Collected'),
        ('processing','Processing'),
        ('completed','Completed'),
        ('cancelled','Cancelled'),
    ]      
    order_id=models.CharField(max_length=20,unique=True)  
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lab_orders')
    order_date=models.DateTimeField()
    status=models.CharField(max_length=20,choices=STATUS_CHOICES, default='pending')
    priority=models.CharField(max_length=20,choices=[
        ('normal','Normal'),
        ('urgent','Urgent'),
        ('stat','STAT'),
    ],default='normal')
    notes=models.TextField(blank=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2)
    collected_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='collected_lab_orders'
    )
    collected_by=models.DateTimeField(null=True,blank=True)
    completed_at=models.DateTimeField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-order_date']
    def __str__(self):
        return f"Lab Order {self.order_id} - {self.patient.full_name}"    

class LabOrderItem(models.Model):
    order=models.ForeignKey(LabOrder,on_delete=models.CASCADE,related_name='items')
    test=models.ForeignKey(LabTest,on_delete=models.CASCADE)   
    quantity=models.IntegerField(default=1)
    unit_prices=models.DecimalField(max_digits=10,decimal_places=2)
    total_prices=models.DecimalField(max_digits=10,decimal_places=2)
    
    def save(self,*args,**kwargs):
        self.unit_prices=self.test.price
        self.total_prices=self.quantity * self.unit_prices
        super().save(*args,**kwargs)
    
    def __str__(self):
        return f"{self.test.name}-{self.quantity}"

class LabResult(models.Model):
    order_item=models.OneToOneField(LabOrderItem,on_delete=models.CASCADE,related_name='result')
    result_value = models.TextField()
    is_normal = models.BooleanField(default=True)
    comments = models.TextField(blank=True)
    tested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lab_results'
    )
    tested_at = models.DateTimeField()
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_lab_results'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Result for {self.order_item.test.name}"         
        