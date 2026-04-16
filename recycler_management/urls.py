from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('add/', views.vendor_create, name='vendor_add'),
    path('edit/<int:id>/', views.vendor_edit, name='vendor_edit'),
    path('delete/<int:id>/', views.vendor_delete, name='vendor_delete'),
]