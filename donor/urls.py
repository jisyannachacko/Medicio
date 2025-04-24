"""blood_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . views import *
from . import views
urlpatterns = [
    path('',medicio,name="medicio"),
    path('bloodhome/', bloodhome,name="blood_home"),
    path('loginaction/', loginaction,name="login"),
    path('logout/', logout,name="logout"),
    path('signupaction/', signaction,name="signup"),
    path('donorreg/', donorreg,name="donate"),
    path('bloodsearch/',bloodsearch,name="search"),
    path('view_result/',view_result,name="viewresult"),
    path('submit_blood_request/', views.submit_blood_request, name='submit_blood_request'),
    path('success/', views.success_page, name='success_page'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('bloodlogin/', bloodlogin,name="bloodlogin"),
        







]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
