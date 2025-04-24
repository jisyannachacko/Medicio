from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from .models import Organ_Users, Organ_Types, Organ_Donor_Register, OrganRequest, OrganInventory
from hospital.models import Hospital_Users

def organhome(request):
    return render(request, 'organ/organ_home.html')

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Organ_Users

from django.shortcuts import render, redirect
from django.http import HttpResponse

def organ_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pass')

        if not email or not password:
            return HttpResponse('Please enter both email and password.')

        user = Organ_Users.objects.filter(E_mail=email, Password=password).first()

        if user:
            request.session['organ_user_id'] = user.pk
            return redirect('organ_dashboard')

        else:
            return HttpResponse('Wrong email or password or account does not exist!')

    return render(request, 'organ/organ_login.html')
def organ_signup(request):
    if request.method == "POST":
        Full_Name = request.POST['fullname']
        E_mail = request.POST['email']
        PH_number = request.POST['number']
        Password = request.POST['pass']

        # Check if user already exists
        if Organ_Users.objects.filter(E_mail=E_mail).exists():
            return HttpResponse('User with this email already exists!')

        # Create new user
        user = Organ_Users(
            Full_Name=Full_Name,
            E_mail=E_mail,
            PH_number=PH_number,
            Password=Password
        )
        user.save()
        return redirect('organ_login')
    return render(request, 'organ/organ_signup.html')

def organ_donor_register(request):
    if request.method == "POST":
        # Basic personal information
        First_Name = request.POST['first']
        Last_Name = request.POST['last']
        Age = request.POST['age']
        Date_Of_Birth = request.POST['birthday']
        Gender = request.POST['gender']
        Address = request.POST['address']
        Hospital = request.POST['hospital']
        PinCode = request.POST['pin']
        District = request.POST['district']
        State = request.POST['state']
        Weight = request.POST['weight']
        Height = request.POST['height']
        Blood_Type = request.POST['blood_type']
        
        # Medical information
        Diabetic = request.POST['diabetic']
        HIV = request.POST['hiv']
        Hepatitis = request.POST['hepatitis']
        Hypertension = request.POST['hypertension']
        Cancer_History = request.POST['cancer']
        Medicine = request.POST['medicine']
        Medicine_Name = request.POST.get('medicine_name', '')
        Disease = request.POST['disease']
        Disease_Name = request.POST.get('disease_name', '')
        Surgery = request.POST['surgery']
        Surgery_Name = request.POST.get('surgery_name', '')
        
        # Organ donation specific information
        Donation_Type = request.POST['donation_type']
        Emergency_Contact_Name = request.POST['emergency_name']
        Emergency_Contact_Number = request.POST['emergency_number']
        Family_Consent = 'family_consent' in request.POST
        
        # Create donor registration
        donor = Organ_Donor_Register(
            First_Name=First_Name,
            Last_Name=Last_Name,
            Age=Age,
            Date_Of_Birth=Date_Of_Birth,
            Gender=Gender,
            Address=Address,
            Hospital=Hospital,
            PinCode=PinCode,
            District=District,
            State=State,
            Weight=Weight,
            Height=Height,
            Blood_Type=Blood_Type,
            Diabetic=Diabetic,
            HIV=HIV,
            Hepatitis=Hepatitis,
            Hypertension=Hypertension,
            Cancer_History=Cancer_History,
            Medicine=Medicine,
            Medicine_Name=Medicine_Name,
            Disease=Disease,
            Disease_Name=Disease_Name,
            Surgery=Surgery,
            Surgery_Name=Surgery_Name,
            Donation_Type=Donation_Type,
            Emergency_Contact_Name=Emergency_Contact_Name,
            Emergency_Contact_Number=Emergency_Contact_Number,
            Family_Consent=Family_Consent,
            status='pending'
        )
        donor.save()
        
        # Add selected organs
        selected_organs = request.POST.getlist('organs')
        for organ_id in selected_organs:
            organ = Organ_Types.objects.get(id=organ_id)
            donor.Organs_Donated.add(organ)
        
        messages.success(request, "Thank you for registering as an organ donor!")
        return redirect('organ_dashboard')
    
    # For GET request, prepare form data
    hospitals = Hospital_Users.objects.all()
    organ_types = Organ_Types.objects.all()
    return render(request, 'organ/donor_register.html', {
        'hospitals': hospitals,
        'organ_types': organ_types
    })

def organ_dashboard(request):
    if 'organ_user_id' not in request.session:
        return redirect('organ_login')
    
    # Get user's actual name from database
    user_id = request.session['organ_user_id']
    user = Organ_Users.objects.get(id=user_id)
    
    return render(request, 'organ/organ_dashboard.html', {
        'user_name': user.Full_Name,
        'user_authenticated': True
    })


def organ_logout(request):
    if 'organ_user_id' in request.session:
        del request.session['organ_user_id']
    return redirect('organhome')

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Organ_Types, OrganInventory

def organ_search(request):
    user_authenticated = 'organ_user_id' in request.session
    user_identifier = request.session.get('user_identifier', '')

    if request.method == 'GET' and 'organ_type' in request.GET:
        organ_type_id = request.GET.get('organ_type')
        district = request.GET.get('district','')
        blood_type = request.GET.get('blood_type', '')

        try:
            organ_type = get_object_or_404(Organ_Types, id=organ_type_id)
            organ_type_name = organ_type.Organ_Name

            # Build query with case-insensitive district matching
            query = Q(organ_type=organ_type, availability_status='available')
            
            if blood_type:
                query &= Q(blood_type=blood_type)

            results = OrganInventory.objects.filter(query).select_related('hospital', 'organ_type')

            return render(request, 'organ/organ_search_results.html', {
                'results': results,
                'organ_type': organ_type_name,
                'district': district.title(),  # Proper case for display
                'blood_type': blood_type,
                'user_authenticated': user_authenticated,
                'user_identifier': user_identifier
            })

        except Organ_Types.DoesNotExist:
            messages.error(request, "Invalid organ type selected")
            return redirect('organ_search')

    # Initial search form
    organ_types = Organ_Types.objects.all()
    return render(request, 'organ/organ_search.html', {
        'organ_types': organ_types,
        'user_authenticated': user_authenticated,
        'user_identifier': user_identifier
    })

def submit_organ_request(request):
    if 'organ_user_id' not in request.session:
        return redirect('organ_login')
    if request.method == 'POST':
        try:
            patient_name = request.POST['patient_name']
            contact_number = request.POST['contact_number']
            email = request.POST['email']
            blood_type = request.POST['blood_type']
            organ_needed_id = request.POST['organ_needed']
            urgency_level = request.POST['urgency_level']
            hospital_name = request.POST['hospital_name']
            medical_documents = request.FILES['medical_documents']
            
            # Get hospital and organ type objects
            try:
                hospital = Hospital_Users.objects.get(Hospital_Name=hospital_name)
                organ_needed = Organ_Types.objects.get(id=organ_needed_id)
            except (Hospital_Users.DoesNotExist, Organ_Types.DoesNotExist):
                messages.error(request, "Hospital or organ type not found in our system")
                return render(request, 'organ/request_form.html')
            
            # Create organ request
            organ_request = OrganRequest.objects.create(
                hospital=hospital,
                patient_name=patient_name,
                contact_number=contact_number,
                email=email,
                blood_type=blood_type,
                organ_needed=organ_needed,
                urgency_level=urgency_level,
                medical_documents=medical_documents
            )
            
            messages.success(request, "Organ request submitted successfully!")
            return redirect('organ_request_success')
            
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'organ/request_form.html')
    
    # For GET requests
    hospitals = Hospital_Users.objects.all()
    organ_types = Organ_Types.objects.all()
    return render(request, 'organ/request_form.html', {
        'hospitals': hospitals,
        'organ_types': organ_types,
        'user_authenticated': True

    })

def organ_request_success(request):
    if 'organ_user_id' not in request.session:
        return redirect('organ_login')
    return render(request, 'organ/request_success.html')

# Hospital-side views for the organ module
def hospital_view_organ_donors(request):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    hospital_name = request.session['id']
    donors = Organ_Donor_Register.objects.filter(Hospital=hospital_name, status='pending')
    return render(request, 'organ/hospital_view_donors.html', {'donors': donors})

def accept_organ_donor(request, donor_id):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    try:
        hospital_name = request.session['id']
        donor = Organ_Donor_Register.objects.get(id=donor_id, Hospital=hospital_name)
        
        if donor.status != 'pending':
            messages.warning(request, "Donor has already been processed")
            return redirect('hospital_view_organ_donors')

        with transaction.atomic():
            donor.status = 'accepted'
            donor.save()
            
            # Add to inventory
            for organ in donor.Organs_Donated.all():
                OrganInventory.objects.create(
                    hospital=Hospital_Users.objects.get(Hospital_Name=hospital_name),
                    organ_type=organ,
                    blood_type=donor.Blood_Type,
                    availability_status='available',
                    donor=donor
                )
            
            messages.success(request, f"Donor {donor.First_Name} accepted and added to inventory")
            
    except Exception as e:
        messages.error(request, f"Error processing donor: {str(e)}")
    
    return redirect('hospital_view_organ_donors')

def reject_organ_donor(request, donor_id):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    try:
        hospital_name = request.session['id']
        donor = Organ_Donor_Register.objects.get(id=donor_id, Hospital=hospital_name)
        
        if donor.status != 'pending':
            messages.warning(request, "Donor has already been processed")
            return redirect('hospital_view_organ_donors')
            
        donor.status = 'rejected'
        donor.save()
        messages.success(request, f"Donor {donor.First_Name} rejected")
        
    except Exception as e:
        messages.error(request, f"Error rejecting donor: {str(e)}")
    
    return redirect('hospital_view_organ_donors')

def hospital_view_organ_requests(request):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    hospital_name = request.session['id']
    
    try:
        hospital = Hospital_Users.objects.get(Hospital_Name=hospital_name)
        requests = OrganRequest.objects.filter(hospital=hospital)
        return render(request, 'organ/hospital_view_requests.html', {'requests': requests})
    except Hospital_Users.DoesNotExist:
        return HttpResponse("Hospital not found")

def approve_organ_request(request, request_id):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    hospital_name = request.session['id']
    
    try:
        with transaction.atomic():
            hospital = Hospital_Users.objects.get(Hospital_Name=hospital_name)
            organ_request = OrganRequest.objects.get(id=request_id, hospital=hospital)
            
            # Check inventory availability
            inventory = OrganInventory.objects.filter(
                hospital=hospital,
                organ_type=organ_request.organ_needed,
                blood_type=organ_request.blood_type,
                availability_status='available'
            ).first()
            
            if not inventory:
                messages.error(request, f"No matching {organ_request.organ_needed.Organ_Name} available")
                return redirect('hospital_view_organ_requests')
            
            # Update request and inventory status
            organ_request.approved = True
            organ_request.save()
            
            inventory.availability_status = 'matched'
            inventory.save()
            
            messages.success(request, f"Request for {organ_request.organ_needed.Organ_Name} approved successfully")
    except Exception as e:
        messages.error(request, f"Error approving request: {str(e)}")
    
    return redirect('hospital_view_organ_requests')

def organ_inventory(request):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    hospital_name = request.session['id']
    
    try:
        hospital = Hospital_Users.objects.get(Hospital_Name=hospital_name)
        inventory = OrganInventory.objects.filter(hospital=hospital)
        
        # Group by organ type for summary
        organ_types = Organ_Types.objects.all()
        summary = {}
        
        for organ_type in organ_types:
            available_count = inventory.filter(
                organ_type=organ_type,
                availability_status='available'
            ).count()
            
            if available_count > 0:
                summary[organ_type.Organ_Name] = available_count
        
        return render(request, 'organ/organ_inventory.html', {
            'inventory': inventory,
            'summary': summary
        })
    except Hospital_Users.DoesNotExist:
        return HttpResponse("Hospital not found")
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Organ_Donor_Register, Organ_Types, Hospital_Users  # Adjust based on your models
from django.contrib.auth.decorators import login_required  # If login is required
from django.http import HttpRequest  # Optional: for type hinting


def kidney_liver_donor_register(request: HttpRequest):
    user_authenticated = 'organ_user_id' in request.session

    if request.method == "POST":
        # Get organ selection
        selected_organ = request.POST.get('selected_organ')
        
        # Basic personal information
        First_Name = request.POST['first']
        Last_Name = request.POST['last']
        Age = request.POST['age']
        Date_Of_Birth = request.POST['birthday']
        Gender = request.POST['gender']
        Address = request.POST['address']
        Hospital = request.POST['hospital']
        PinCode = request.POST['pin']
        District = request.POST['district']
        State = request.POST['state']
        Weight = request.POST['weight']
        Height = request.POST['height']
        Blood_Type = request.POST['blood_type']
        
        # Specific kidney/liver tests
        liver_tests_done = 'liver_tests_done' in request.POST
        kidney_tests_done = 'kidney_tests_done' in request.POST
        
        # Medical information
        Diabetic = request.POST['diabetic']
        HIV = request.POST['hiv']
        Hepatitis = request.POST['hepatitis']
        Hypertension = request.POST['hypertension']
        Cancer_History = request.POST['cancer']
        Medicine = request.POST['medicine']
        Medicine_Name = request.POST.get('medicine_name', '')
        Disease = request.POST['disease']
        Disease_Name = request.POST.get('disease_name', '')
        Surgery = request.POST['surgery']
        Surgery_Name = request.POST.get('surgery_name', '')
        
        # Organ donation specific information
        Donation_Type = request.POST['donation_type']
        Emergency_Contact_Name = request.POST['emergency_name']
        Emergency_Contact_Number = request.POST['emergency_number']
        Family_Consent = 'family_consent' in request.POST
        Understand_Risks = 'understand_risks' in request.POST
        
        # Create donor registration
        donor = Organ_Donor_Register(
            First_Name=First_Name,
            Last_Name=Last_Name,
            Age=Age,
            Date_Of_Birth=Date_Of_Birth,
            Gender=Gender,
            Address=Address,
            Hospital=Hospital,
            PinCode=PinCode,
            District=District,
            State=State,
            Weight=Weight,
            Height=Height,
            Blood_Type=Blood_Type,
            Diabetic=Diabetic,
            HIV=HIV,
            Hepatitis=Hepatitis,
            Hypertension=Hypertension,
            Cancer_History=Cancer_History,
            Medicine=Medicine,
            Medicine_Name=Medicine_Name,
            Disease=Disease,
            Disease_Name=Disease_Name,
            Surgery=Surgery,
            Surgery_Name=Surgery_Name,
            Donation_Type=Donation_Type,
            Emergency_Contact_Name=Emergency_Contact_Name,
            Emergency_Contact_Number=Emergency_Contact_Number,
            Family_Consent=Family_Consent,
            status='pending'
        )
        donor.save()
        
        # Add selected organs
        kidney_organ = Organ_Types.objects.get(Organ_Name='Kidney')
        liver_organ = Organ_Types.objects.get(Organ_Name='Liver')
        
        if selected_organ == 'kidney':
            donor.Organs_Donated.add(kidney_organ)
        elif selected_organ == 'liver':
            donor.Organs_Donated.add(liver_organ)
        elif selected_organ == 'both':
            donor.Organs_Donated.add(kidney_organ, liver_organ)
        
        messages.success(request, "Thank you for registering as a kidney/liver donor!")
        return redirect('organ_dashboard')
    
    # Handle GET request
    hospitals = Hospital_Users.objects.all()
    
    # Example of how to get auth status and identifier
    user_is_authenticated = request.user.is_authenticated
    user_identifier = request.user.username if user_is_authenticated else None

    context = {
        'user_authenticated': user_authenticated,

        'hospitals': hospitals,
    }


    return render(request, 'organ/kidney_liver_register.html', context)

# your_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Organ_Donor_Register, Organ_Types # Make sure Organ_Types is imported if used in Organs_Donated
from django.contrib.auth.decorators import login_required # Consider using built-in login_required

# Assuming Organ_Types model exists and is imported
# from .models import Organ_Types # Import if needed

# Optional: Decorator for login check
# @login_required
def hospital_view_organ_donors(request):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    hospital_name = request.session['id']
    donors = Organ_Donor_Register.objects.filter(Hospital=hospital_name).order_by('-registration_date')
    return render(request, 'organ/hospital_view_donors.html', {'donors': donors})

# Optional: Decorator for login check and only allowing AJAX requests
# from django.views.decorators.http import require_ajax
# @login_required
# @require_ajax
def get_donor_details(request, donor_id):
    # Use decorator or keep manual check
    if 'id' not in request.session:
        return JsonResponse({'error': 'Unauthorized'}, status=401) # Use 401 for unauthorized

    hospital_name = request.session['id']

    try:
        # Fetch the donor and ensure they belong to the hospital
        donor = Organ_Donor_Register.objects.get(id=donor_id, Hospital=hospital_name)
        organs_list = [organ.Organ_Name for organ in donor.Organs_Donated.all()]

        donor_data = {
            'first_name': donor.First_Name,
            'last_name': donor.Last_Name,
            'age': donor.Age,
            'date_of_birth': donor.Date_Of_Birth,
            'gender': donor.Gender,
            'address': donor.Address,
            'pincode': donor.PinCode,
            'district': donor.District,
            'state': donor.State,
            'weight': donor.Weight,
            'height': donor.Height,
            'blood_type': donor.Blood_Type,
            'diabetic': donor.Diabetic,
            'hiv': donor.HIV,
            'hepatitis': donor.Hepatitis,
            'hypertension': donor.Hypertension,
            'cancer_history': donor.Cancer_History,
            'medicine': donor.Medicine,
            'medicine_name': donor.Medicine_Name,
            'disease': donor.Disease,
            'disease_name': donor.Disease_Name,
            'surgery': donor.Surgery,
            'surgery_name': donor.Surgery_Name,
            'organs_donated': organs_list, # Use the list of names
            'donation_type': donor.Donation_Type,
            'status': donor.status # Assuming 'status' field exists
        }
        return JsonResponse(donor_data)

    except Organ_Donor_Register.DoesNotExist:
        return JsonResponse({'error': 'Donor not found or does not belong to this hospital'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def donor_details(request, donor_id):
    if 'id' not in request.session:
        return redirect('hosp_login')
    
    hospital_name = request.session['id']
    
    try:
        donor = Organ_Donor_Register.objects.get(
            id=donor_id,
            Hospital=hospital_name
        )
        return render(request, 'organ/donor_details.html', {'donor': donor})
    
    except Organ_Donor_Register.DoesNotExist:
        messages.error(request, "Donor not found or access denied")
        return redirect('hospital_view_organ_donors')