from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
 
urlpatterns = [
 
    # Django admin panel
    path('admin/', admin.site.urls),
 
    # Accounts — login/logout
    path('', include('accounts.urls')),

    path('rbac/', include('rbac.urls')),

    path('schools/', include('schools.urls')),

    path('vendors/', include('recycler_management.urls')),

    path('esg/', include('esg_tracking.urls')),

    path('waste/', include('waste_management.urls')),
    
  
 
    # Root URL → login page pe redirect
    path('', lambda request: redirect('login'), name='home'),
 
]
 