from django.urls import path
from . import views

urlpatterns = [
    path('', views.school_list, name='school_list'),
    path('add/', views.school_create, name='school_add'),
    path('edit/<int:id>/', views.school_edit, name='school_edit'),
    path('delete/<int:id>/', views.school_delete, name='school_delete'),
    # Reporting Year URLs
    path('<int:school_id>/reporting-years/', views.reporting_year_list, name='reporting_year_list'),
    path('<int:school_id>/reporting-years/add/', views.reporting_year_create, name='reporting_year_add'),
    path('reporting-years/edit/<int:id>/', views.reporting_year_edit, name='reporting_year_edit'),
    path('reporting-years/delete/<int:id>/', views.reporting_year_delete, name='reporting_year_delete'),
    path('reporting-years/activate/<int:id>/', views.reporting_year_activate, name='reporting_year_activate'),
    path('reporting-years/lock/<int:id>/', views.reporting_year_lock, name='reporting_year_lock'),
    # Principal URLs
    path('principals/', views.principal_list, name='principal_list'),
    path('principals/add/', views.principal_create, name='principal_add'),
    path('principals/edit/<int:id>/', views.principal_edit, name='principal_edit'),
    path('principals/delete/<int:id>/', views.principal_delete, name='principal_delete'),
    path('principals/reset-password/<int:id>/', views.principal_reset_password, name='principal_reset_password'),
]