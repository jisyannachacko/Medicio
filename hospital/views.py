from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render,redirect
from .models import *
from donor.models import Blood_Donor_register


# Create your views here.
def hospitalhome(request):
    return render(request, 'hospital_home.html')


def hospitallogin(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        password = request.POST.get('password')
        user = Hospital_Users.objects.filter(E_mail=email, Password=password)
        if user:
            user_details = Hospital_Users.objects.get(E_mail=email, Password=password)
            user_id = user_details.Hospital_Name
            request.session['id'] = user_id
            return render(request, 'hospital_services.html',{'id':user_id})
        else:
            return HttpResponse('wrong user name or password or account does not exist!!')
    return render(request,'hospital_login.html')


def hospitalsignup(request):
    if request.method == "POST":

        HospName = request.POST['hospname']
        address = request.POST['address']
        district = request.POST['district']
        pincode = request.POST['pin']
        PH_number = request.POST['phone']
        E_mail = request.POST['email']
        Password = request.POST['password']

        ob = Hospital_Users()
        ob.Hospital_Name = HospName
        ob.Address1 = address
        ob.District = district
        ob.PinCode = pincode
        ob.PH_number = PH_number
        ob.E_mail = E_mail
        ob.Password = Password
        if (Hospital_Users.objects.filter(E_mail=E_mail)).exists():
            return HttpResponse('User name already exist!!')
        ob.status = 0
        ob.save()
        return render(request, 'hospital_registration.html')
    else:
        return render(request, 'hospital_registration.html')

    return render(request, 'hospital_registration.html')

def logout(request):
    request.session.flush()
    return render(request, 'home_page.html')


def bloodinventory(request):

    num1 = Blood_Stock.objects.filter(Blood_Type='A+').count()
    num2 = Blood_Stock.objects.filter(Blood_Type='A-').count()
    num3 = Blood_Stock.objects.filter(Blood_Type='B+').count()
    num4 = Blood_Stock.objects.filter(Blood_Type='B-').count()
    num5 = Blood_Stock.objects.filter(Blood_Type='AB+').count()
    num6 = Blood_Stock.objects.filter(Blood_Type='AB-').count()
    num7 = Blood_Stock.objects.filter(Blood_Type='O+').count()
    num8 = Blood_Stock.objects.filter(Blood_Type='O-').count()

    return render(request, 'blood_inventory.html',{'Ap':num1,'An':num2,'Bp':num3,'Bn':num4,'ABp':num5,'ABn':num6,'Op':num7,'On':num8})

def hospitalservice(request):
    userid = request.session['id']

    return render(request, 'hospital_services.html',{'id':userid})

def blooddetails(request):
    try:
        userid = request.session['id']
        data=Blood_Donor_register.objects.filter(Hospital=userid,status='pending')
        btyp=Blood_Donor_register.objects.get(Hospital=userid,status='pending')
        bt=btyp.Blood_Type
        request.session['b_type'] = bt
    except:
        return render(request, 'donor_table.html')

    return render(request, 'donor_table.html',{'register':data})


def accept(request, donor_id):  # Add donor_id parameter
    try:
        userid = request.session['id']
        # Get the specific donor using donor_id
        breg = Blood_Donor_register.objects.get(id=donor_id, Hospital=userid, status='pending')
        
        h_det = Hospital_Users.objects.get(Hospital_Name=userid)
        dis = h_det.District
        b_type = breg.Blood_Type  # Get blood type directly from the donor
        
        # Create Blood_Stock entry
        bs = Blood_Stock(Hospital_Name=userid, Blood_Type=b_type, District=dis)
        bs.save()
        
        # Update donor status
        breg.status = 'accepted'
        breg.save()
        return redirect('blood_details')  # Redirect back to donor list
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")

def reject(request, donor_id):  # Add donor_id parameter
    try:
        userid = request.session['id']
        breg = Blood_Donor_register.objects.get(id=donor_id, Hospital=userid, status='pending')
        breg.status = 'rejected'  # Correct status to 'rejected'
        breg.save()
        return redirect('blood_details')  # Redirect back to donor list
        
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")







from django.contrib.auth.decorators import login_required
from donor.models import BloodRequest


from django.contrib import messages
from django.db import transaction

def approve_request(request, request_id):
    hospital_name = request.session.get('id')
    
    if not hospital_name:
        return redirect('hosp_login')
    
    try:
        with transaction.atomic():  # Use transaction to ensure data consistency
            # Get the blood request
            blood_request = BloodRequest.objects.get(id=request_id)
            hospital = Hospital_Users.objects.get(Hospital_Name=hospital_name)
            
            # Verify this request belongs to the logged-in hospital
            if blood_request.hospital != hospital:
                return HttpResponseBadRequest("Unauthorized request")
            
            # Check if the hospital has enough blood stock
            blood_type = blood_request.blood_type
            units_needed = blood_request.units_needed
            
            # Count available blood units of the requested type
            available_units = Blood_Stock.objects.filter(
                Hospital_Name=hospital_name, 
                Blood_Type=blood_type
            ).count()
            
            if available_units < units_needed:
                messages.error(request, f"Insufficient blood stock. Available: {available_units}, Needed: {units_needed}")
                return redirect('view_requests')
            
            # Update the request status
            blood_request.approved = True
            blood_request.save()
            
            # Reduce the blood stock by deleting the required units
            # This assumes each Blood_Stock entry is one unit
            stock_to_use = Blood_Stock.objects.filter(
                Hospital_Name=hospital_name, 
                Blood_Type=blood_type
            )[:units_needed]
            
            # Delete the used stock entries
            for stock in stock_to_use:
                stock.delete()
            
            messages.success(request, f"Blood request for {blood_request.patient_name} approved successfully")
            return redirect('view_requests')
    
    except BloodRequest.DoesNotExist:
        return HttpResponseBadRequest("Request not found")
    except Hospital_Users.DoesNotExist:
        return HttpResponseBadRequest("Hospital not found")
# ... (other imports and views) ...

def view_requests(request):
    # Get the current hospital from the session
    hospital_name = request.session.get('id')

    if not hospital_name:
        return redirect('hosp_login')  # Redirect to login if not logged in

    # Get the hospital object
    try:
        hospital = Hospital_Users.objects.get(Hospital_Name=hospital_name)
        # Get all blood requests for this hospital
        requests = BloodRequest.objects.filter(hospital=hospital)
        # FIX: Change 'view_requests.html' to 'hospital/view_requests.html'
        return render(request, 'hospital/view_requests.html', {'requests': requests}) 
    except Hospital_Users.DoesNotExist:
        return HttpResponseBadRequest("Hospital not found")

