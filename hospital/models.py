from django.db import models


# Create your models here.
class Hospital_Users(models.Model):

    Hospital_Name = models.CharField(max_length=30)
    Address1 = models.CharField(max_length=1024)
    District = models.CharField(max_length=30)
    PinCode = models.CharField(max_length=8)
    PH_number = models.CharField(max_length=30)
    E_mail = models.CharField(max_length=50)
    Password = models.CharField(max_length=30)

    def __str__(self):
        return self.Hospital_Name

class Blood_Stock(models.Model):
    Hospital_Name = models.CharField(max_length=30)
    District=models.CharField(max_length=30,default='district')
    Blood_Type=models.CharField(max_length=5)


    def __str__(self):
        return self.Hospital_Name

class Blood_Result(models.Model):
    Users=models.CharField(max_length=30)
    Blood_Type=models.CharField(max_length=5)
    Result=models.CharField(max_length=10)

    def __str__(self):
        return self.Users