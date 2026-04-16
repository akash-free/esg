from django.urls import path
from . import views
 
urlpatterns = [
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('superadmin/dashboard/', views.superadmin_dashboard, name='superadmin_dashboard'),
    path('change-password/', views.change_password, name='change_password'),
    path('principal/dashboard/', views.principal_dashboard, name='principal_dashboard'),
    path('set-password/<str:token>/', views.change_password_with_token, name='set_password'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('export-dashboard-pdf/', views.export_dashboard_pdf, name='export_dashboard_pdf'),
    path('export-excel/', views.export_waste_excel, name='export_waste_excel'),
    path('export-category-excel/', views.export_category_excel, name='export_category_excel'),
    path('export-monthly-trend-excel/', views.export_monthly_trend_excel, name='export_monthly_trend_excel'),
    path('export-principal-dashboard-pdf/', views.export_principal_dashboard_pdf, name='export_principal_dashboard_pdf'),
    path('export-waste-excel/', views.export_principal_waste_excel, name='export_principal_waste_excel'),
    
]