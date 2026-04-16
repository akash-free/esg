from django.urls import path
from . import views

urlpatterns = [
    # Role URLs
    path('roles/', views.role_list, name='role_list'),
    path('roles/create/', views.role_create, name='role_create'),
    path('roles/edit/<int:id>/', views.role_edit, name='role_edit'),
    path('roles/delete/<int:id>/', views.role_delete, name='role_delete'),
    
    # Menu URLs
    path('menus/', views.menu_list, name='menu_list'),
    path('menus/create/', views.menu_create, name='menu_create'),
    path('menus/edit/<int:id>/', views.menu_edit, name='menu_edit'),
    path('menus/delete/<int:id>/', views.menu_delete, name='menu_delete'),
    
    # Permission URLs
    path('permissions/', views.permission_list, name='permission_list'),
    path('permissions/create/', views.permission_create, name='permission_create'),
    path('permissions/edit/<int:id>/', views.permission_edit, name='permission_edit'),
    path('permissions/delete/<int:id>/', views.permission_delete, name='permission_delete'),
]