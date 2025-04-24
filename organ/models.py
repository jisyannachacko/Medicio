from django.db import models
from hospital.models import Hospital_Users

class Organ_Users(models.Model):
    Full_Name = models.CharField(max_length=30)
    E_mail = models.CharField(max_length=50)
    PH_number = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    
    def __str__(self):
        return self.Full_Name

class Organ_Types(models.Model):
    Organ_Name = models.CharField(max_length=30)
    Description = models.TextField(null=True, blank=True)
    # Flag to indicate if this organ is eligible for living donation
    Living_Donation_Eligible = models.BooleanField(default=False)
    # Average viability time in hours after harvesting
    Viability_Hours = models.PositiveIntegerField(default=24)
    
    def __str__(self):
        return self.Organ_Name

class OrganDonorSelections(models.Model):
    """Track specific organ donation selections and additional requirements"""
    donor = models.ForeignKey('Organ_Donor_Register', on_delete=models.CASCADE, related_name='donor_selections')
    organ_type = models.ForeignKey(Organ_Types, on_delete=models.CASCADE)
    # Fields specific to kidney donations
    is_kidney = models.BooleanField(default=False)
    kidney_function_test_completed = models.BooleanField(default=False)
    kidney_side = models.CharField(max_length=10, choices=[
        ('left', 'Left Kidney'),
        ('right', 'Right Kidney'),
        ('either', 'Either Kidney')
    ], default='either')
    
    # Fields specific to liver donations
    is_liver = models.BooleanField(default=False)
    liver_function_test_completed = models.BooleanField(default=False)
    liver_portion = models.CharField(max_length=20, choices=[
        ('left_lobe', 'Left Lobe'),
        ('right_lobe', 'Right Lobe'),
        ('segment', 'Segment'),
        ('any', 'Any Portion')
    ], default='any')
    
    # Additional medical information that may be required for specific organ donations
    additional_tests_completed = models.BooleanField(default=False)
    specialist_consultation = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('donor', 'organ_type')
        verbose_name = "Organ Donor Selection"
        verbose_name_plural = "Organ Donor Selections"
        
    def __str__(self):
        return f"{self.donor} - {self.organ_type.Organ_Name}"

class Organ_Donor_Register(models.Model):
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    Age = models.PositiveIntegerField()
    Date_Of_Birth = models.CharField(max_length=10)
    Gender = models.CharField(max_length=10)
    Address = models.CharField(max_length=1024)
    PinCode = models.CharField(max_length=8)
    District = models.CharField(max_length=30, null=True)
    Hospital = models.CharField(max_length=80, null=True)
    State = models.CharField(max_length=15)
    Weight = models.FloatField(max_length=6)
    Height = models.FloatField(max_length=6, null=True)
    Blood_Type = models.CharField(max_length=3)
    # Medical conditions related to organ donation
    Diabetic = models.CharField(max_length=5)
    HIV = models.CharField(max_length=5)
    Hepatitis = models.CharField(max_length=5, null=True)
    Hypertension = models.CharField(max_length=5, null=True)
    Cancer_History = models.CharField(max_length=5, null=True)
    Medicine = models.CharField(max_length=5)
    Medicine_Name = models.CharField(max_length=30, null=True)
    Disease = models.CharField(max_length=5)
    Disease_Name = models.CharField(max_length=30, null=True)
    Surgery = models.CharField(max_length=5)
    Surgery_Name = models.CharField(max_length=30, null=True)
    # Organ donation specific fields
    Organs_Donated = models.ManyToManyField(Organ_Types, related_name="donors")
    Donation_Type = models.CharField(max_length=20, choices=[
        ('living', 'Living Donor'),
        ('deceased', 'Deceased Donor')
    ])
    Emergency_Contact_Name = models.CharField(max_length=50)
    Emergency_Contact_Number = models.CharField(max_length=15)
    Family_Consent = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default='pending')
    # New fields for kidney and liver specific donation
    kidney_donation = models.BooleanField(default=False)
    liver_donation = models.BooleanField(default=False)
    # Advanced consent and verification
    understood_risks = models.BooleanField(default=False)
    medical_evaluation_complete = models.BooleanField(default=False)
    psychological_evaluation_complete = models.BooleanField(default=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.First_Name} {self.Last_Name}"
    
    def save(self, *args, **kwargs):
        # Set kidney_donation and liver_donation based on Organs_Donated
        # This will be updated after saving if Organs_Donated are modified
        super().save(*args, **kwargs)

class OrganRequest(models.Model):
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
    organ_needed = models.ForeignKey(Organ_Types, on_delete=models.CASCADE)
    urgency_level = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ])
    medical_documents = models.FileField(upload_to='organ_request_docs/')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    # Additional fields for kidney and liver requests
    is_kidney_request = models.BooleanField(default=False)
    is_liver_request = models.BooleanField(default=False)
    specific_requirements = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('hospital', 'patient_name', 'organ_needed')
    
    def __str__(self):
        return f"{self.patient_name} - {self.organ_needed.Organ_Name} - {self.hospital.Hospital_Name}"
    
    def save(self, *args, **kwargs):
        # Automatically set is_kidney_request and is_liver_request based on organ_needed
        if self.organ_needed_id:
            try:
                organ = Organ_Types.objects.get(id=self.organ_needed_id)
                self.is_kidney_request = (organ.Organ_Name.lower() == 'kidney')
                self.is_liver_request = (organ.Organ_Name.lower() == 'liver')
            except Organ_Types.DoesNotExist:
                pass
        super().save(*args, **kwargs)

class OrganInventory(models.Model):
    hospital = models.ForeignKey(Hospital_Users, on_delete=models.CASCADE)
    organ_type = models.ForeignKey(Organ_Types, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3)
    availability_status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('matched', 'Matched'),
        ('transplanted', 'Transplanted')
    ])
    preservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    donor = models.ForeignKey(Organ_Donor_Register, on_delete=models.SET_NULL, null=True)
    
    # Additional fields for kidney and liver inventory
    is_kidney = models.BooleanField(default=False)
    kidney_side = models.CharField(max_length=10, choices=[
        ('left', 'Left Kidney'),
        ('right', 'Right Kidney')
    ], null=True, blank=True)
    
    is_liver = models.BooleanField(default=False)
    liver_portion = models.CharField(max_length=20, choices=[
        ('left_lobe', 'Left Lobe'),
        ('right_lobe', 'Right Lobe'),
        ('segment', 'Segment'),
        ('whole', 'Whole Liver')
    ], null=True, blank=True)
    
    organ_condition = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair')
    ], default='good')
    
    def __str__(self):
        return f"{self.organ_type.Organ_Name} - {self.blood_type} - {self.hospital.Hospital_Name}"
    
    def save(self, *args, **kwargs):
        # Automatically set is_kidney and is_liver based on organ_type
        if self.organ_type_id:
            try:
                organ = Organ_Types.objects.get(id=self.organ_type_id)
                self.is_kidney = (organ.Organ_Name.lower() == 'kidney')
                self.is_liver = (organ.Organ_Name.lower() == 'liver')
            except Organ_Types.DoesNotExist:
                pass
        super().save(*args, **kwargs)