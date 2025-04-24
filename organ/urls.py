from django.urls import path
from . import views

urlpatterns = [
    # User-facing views
    path('', views.organhome, name='organhome'),
    path('login/', views.organ_login, name='organ_login'),
    path('signup/', views.organ_signup, name='organ_signup'),
    path('logout/', views.organ_logout, name='organ_logout'),
    path('dashboard/', views.organ_dashboard, name='organ_dashboard'),
    path('register/', views.organ_donor_register, name='organ_donor_register'),
    # New route for kidney and liver donation
    path('register/kidney-liver/', views.kidney_liver_donor_register, name='kidney_liver_donor_register'),
    path('search/', views.organ_search, name='organ_search'),
    path('request/', views.submit_organ_request, name='submit_organ_request'),
    path('request/success/', views.organ_request_success, name='organ_request_success'),
    
    
    # Hospital-facing views
    path('hospital/donors/', views.hospital_view_organ_donors, name='hospital_view_organ_donors'),
    path('hospital/donors/accept/<int:donor_id>/', views.accept_organ_donor, name='accept_organ_donor'),
    path('hospital/donors/reject/<int:donor_id>/', views.reject_organ_donor, name='reject_organ_donor'),
    path('hospital/requests/', views.hospital_view_organ_requests, name='hospital_view_organ_requests'),
    path('hospital/requests/approve/<int:request_id>/', views.approve_organ_request, name='approve_organ_request'),
    path('hospital/inventory/', views.organ_inventory, name='organ_inventory'),
    path('get-donor-details/<int:donor_id>/', views.get_donor_details, name='get_donor_details_ajax'),
            path('hospital/donors/<int:donor_id>/', views.donor_details, name='donor_details'),


]