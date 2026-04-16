from django.contrib import admin
from .models import WasteCategory, WasteSubCategory, TreatmentMethod, ESGFactor


@admin.register(WasteCategory)
class WasteCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'icon', 'order', 'is_active')
        }),
    )


@admin.register(WasteSubCategory)
class WasteSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'tree_type', 'order', 'is_active']
    list_filter = ['category', 'is_active', 'tree_type']
    search_fields = ['name', 'category__name']
    list_editable = ['order', 'is_active']
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description', 'order', 'is_active')
        }),
        ('Paper Specific Fields (for Paper category only)', {
            'fields': ('tree_type', 'growth_rate_years', 'co2_absorption'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TreatmentMethod)
class TreatmentMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'co2_effect', 'water_effect', 'order', 'is_active']
    list_filter = ['co2_effect', 'water_effect', 'is_active']
    search_fields = ['name']
    list_editable = ['order', 'is_active']


@admin.register(ESGFactor)
class ESGFactorAdmin(admin.ModelAdmin):
    list_display = ['sub_category', 'treatment', 'co2_factor', 'water_factor', 'trees_factor', 'updated_at']
    list_filter = ['sub_category__category', 'treatment']
    search_fields = ['sub_category__name', 'sub_category__category__name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Selection', {
            'fields': ('sub_category', 'treatment')
        }),
        ('Impact Factors', {
            'fields': ('co2_factor', 'water_factor', 'trees_factor', 'energy_factor')
        }),
        ('Source Information', {
            'fields': ('source_standard', 'notes')
        }),
        ('Audit', {
            'fields': ('last_edited_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user.username
        super().save_model(request, obj, form, change)