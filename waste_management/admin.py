from django.contrib import admin
from .models import WasteEntry

@admin.register(WasteEntry)
class WasteEntryAdmin(admin.ModelAdmin):
    list_display = ['entry_date', 'reporting_year', 'waste_category', 'weight_kg', 'treatment_method', 'co2e_kg']
    list_filter = ['waste_category', 'treatment_method', 'entry_date']
    search_fields = ['waste_category', 'vendor_name']
    readonly_fields = ['emission_factor_used', 'co2e_kg', 'water_saved_litres', 'trees_equivalent']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('reporting_year', 'entry_date', 'source', 'waste_category', 'weight_kg', 'treatment_method', 'vendor_name')
        }),
        ('Auto-calculated (Read Only)', {
            'fields': ('emission_factor_used', 'co2e_kg', 'water_saved_litres', 'trees_equivalent')
        }),
    )