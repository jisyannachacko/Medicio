from django.contrib import admin
from .models import Organ_Users, Organ_Types, Organ_Donor_Register, OrganRequest, OrganInventory

class Organ_UsersAdmin(admin.ModelAdmin):
    list_display = ('Full_Name', 'E_mail', 'PH_number')
    search_fields = ('Full_Name', 'E_mail')

class Organ_TypesAdmin(admin.ModelAdmin):
    list_display = ('Organ_Name', 'Description')
    search_fields = ('Organ_Name',)

class Organ_Donor_RegisterAdmin(admin.ModelAdmin):
    list_display = ('First_Name', 'Last_Name', 'Age', 'Blood_Type', 'Hospital', 'status')
    list_filter = ('Blood_Type', 'status', 'Donation_Type', 'Gender')
    search_fields = ('First_Name', 'Last_Name', 'Hospital')
    filter_horizontal = ('Organs_Donated',)

class OrganRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'organ_needed', 'blood_type', 'hospital', 'urgency_level', 'approved')
    list_filter = ('blood_type', 'urgency_level', 'approved')
    search_fields = ('patient_name', 'hospital__Hospital_Name')

class OrganInventoryAdmin(admin.ModelAdmin):
    list_display = ('organ_type', 'blood_type', 'hospital', 'availability_status')
    list_filter = ('availability_status', 'blood_type')
    search_fields = ('hospital__Hospital_Name', 'organ_type__Organ_Name')

admin.site.register(Organ_Users, Organ_UsersAdmin)
admin.site.register(Organ_Types, Organ_TypesAdmin)
admin.site.register(Organ_Donor_Register, Organ_Donor_RegisterAdmin)
admin.site.register(OrganRequest, OrganRequestAdmin)
admin.site.register(OrganInventory, OrganInventoryAdmin)