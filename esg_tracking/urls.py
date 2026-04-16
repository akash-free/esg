from django.urls import path
from . import views

urlpatterns = [
    # Waste Category URLs
    path('categories/', views.category_list, name='esg_category_list'),
    path('categories/create/', views.category_create, name='esg_category_create'),
    path('categories/edit/<int:id>/', views.category_edit, name='esg_category_edit'),
    path('categories/delete/<int:id>/', views.category_delete, name='esg_category_delete'),
    
    # Sub-Category URLs
    path('subcategories/', views.subcategory_list, name='esg_subcategory_list'),
    path('subcategories/create/', views.subcategory_create, name='esg_subcategory_create'),
    path('subcategories/edit/<int:id>/', views.subcategory_edit, name='esg_subcategory_edit'),
    path('subcategories/delete/<int:id>/', views.subcategory_delete, name='esg_subcategory_delete'),
    
    # Treatment Method URLs
    path('treatments/', views.treatment_list, name='esg_treatment_list'),
    path('treatments/create/', views.treatment_create, name='esg_treatment_create'),
    path('treatments/edit/<int:id>/', views.treatment_edit, name='esg_treatment_edit'),
    path('treatments/delete/<int:id>/', views.treatment_delete, name='esg_treatment_delete'),
    
    # ESG Factor URLs
    path('factors/', views.esg_factor_list, name='esg_factor_list'),
    path('factors/create/', views.esg_factor_create, name='esg_factor_create'),
    path('factors/edit/<int:id>/', views.esg_factor_edit, name='esg_factor_edit'),
    path('factors/delete/<int:id>/', views.esg_factor_delete, name='esg_factor_delete'),
    path('api/sub-categories/', views.get_sub_categories, name='api_sub_categories'),
    path('api/esg-factor/', views.get_esg_factor, name='api_esg_factor'),
    path('api/category-defaults/', views.get_category_defaults, name='api_category_defaults'),
]