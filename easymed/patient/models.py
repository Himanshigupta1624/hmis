from django.db import models
from django.conf import settings

class Patient(models.Model):
    GENDER_CHOICES=[
        ('M','Male'),
        ('F','Female'),
        ('O','Other'),
    ]
    BLOOD_GROUP_CHOICES=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
        
    ]
    patient_id=models.CharField(max_length=20,unique=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    date_of_birth=models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_phone = models.CharField(max_length=15)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.paitent_id})"   
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today=date.today()
        return today.year-self.date_of_birth   -((today.month,today.day)<(self.date_of_birth.month,self.date_of_birth.day)) 

class PatientVisit(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='visits')
    visit_date=models.DateTimeField()
    doctor=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-visit_date']
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.visit_date.strftime('%Y-%m-%d')}"
