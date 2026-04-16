from django.urls import path
from . import views



urlpatterns = [
    path('add/', views.waste_entry_add, name='waste_entry_add'),
    path('my-entries/', views.waste_entry_list, name='waste_entry_list'),
    path('edit/<int:id>/', views.waste_entry_edit, name='waste_entry_edit'),
    path('delete/<int:id>/', views.waste_entry_delete, name='waste_entry_delete'),
]