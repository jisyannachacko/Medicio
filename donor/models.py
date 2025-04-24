from django.db import models
from django.contrib.auth.models import User
from hospital.models import Hospital_Users

class Blood_Users(models.Model):
    Full_Name = models.CharField(max_length=30)
    E_mail = models.CharField(max_length=50)
    PH_number = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    def __str__(self):
        return self.Full_Name

class Blood_Donor_register(models.Model):
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    Age = models.PositiveIntegerField(null=False, blank=False)
    Blood_Type = models.CharField(max_length=3)
    Date_Of_Birth = models.CharField(max_length=10)
    Gender = models.CharField(max_length=10)
    Address = models.CharField(max_length=1024)
    PinCode = models.CharField(max_length=8)
    District = models.CharField(max_length=30, null=True)
    Hospital = models.CharField(max_length=80,null=True)
    State = models.CharField(max_length=15)
    Weight = models.FloatField(max_length=6)
    Diabetic = models.CharField(max_length=5)
    HIV = models.CharField(max_length=5)
    Medicine = models.CharField(max_length=5)
    Medicine_Name = models.CharField(max_length=30, null=True)
    Disease = models.CharField(max_length=5)
    Disease_Name = models.CharField(max_length=30, null=True)
    Surgery = models.CharField(max_length=5)
    Surgery_Name = models.CharField(max_length=30, null=True)
    Donated_Previous = models.CharField(max_length=5)
    Donated_Date = models.CharField(max_length=10,null=True)
    status=models.CharField(max_length=10,null=True)
    def __str__(self):
        return self.First_Name
    

class BloodRequest(models.Model):
    hospital = models.ForeignKey(Hospital_Users, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    blood_type = models.CharField(max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ])
    units_needed = models.PositiveIntegerField(default=1)
    document = models.FileField(upload_to='blood_request_docs/')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('hospital', 'patient_name')  # Enforces unique name per hospital

    def __str__(self):
        return f"{self.patient_name} - {self.hospital.Hospital_Name}"

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.email}"