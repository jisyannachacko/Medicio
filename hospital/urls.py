
from django.urls import path
from . views import *
from . import views
from donor.views import submit_blood_request

urlpatterns = [

    path('hospitalhome/', hospitalhome, name="hosp_home"),
    path('hospitallogin/', hospitallogin, name="hosp_login"),
    path('hospitalsignup/', hospitalsignup, name="hosp_reg"),
    path('logout/', logout,name="logout"),
    path('blooddetails/',blooddetails,name="blood_details"),
    path('bloodinventory/', bloodinventory, name="blood_inv"),
    path('hospitalservice/', hospitalservice, name="hosp_serv"),
    path('accept/<int:donor_id>/', accept, name="add"),
    path('reject/<int:donor_id>/', reject, name="rej"),
    path('submit-blood-request/', submit_blood_request, name='submit_blood_request'),
    path('requests/', views.view_requests, name='view_requests'),
    path('requests/approve/<int:request_id>/', views.approve_request, name='approve_request'),

]