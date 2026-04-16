from django.contrib import admin
from .models import Material, Recycler, RecyclerMaterial


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['material_name', 'unit', 'is_active']
    list_filter = ['is_active']
    search_fields = ['material_name']
    list_editable = ['is_active']


@admin.register(Recycler)
class RecyclerAdmin(admin.ModelAdmin):
    list_display = ['recycler_name', 'vendor_type', 'city', 'trust_score', 'status']
    list_filter = ['vendor_type', 'status', 'city']
    search_fields = ['recycler_name', 'contact_email', 'contact_phone']
    list_editable = ['trust_score', 'status']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('recycler_name', 'vendor_type', 'status')
        }),
        ('Address & Contact', {
            'fields': ('address', 'city', 'state', 'pincode', 'contact_person', 'contact_email', 'contact_phone')
        }),
        ('Business Information', {
            'fields': ('gst_number', 'certifications')
        }),
        ('Operational Information', {
            'fields': ('processing_capacity', 'recycling_efficiency', 'minimum_quantity', 'pickup_schedule', 'service_cities')
        }),
        ('Performance Metrics', {
            'fields': ('trust_score', 'total_collected', 'total_processed', 'certificates_issued')
        }),
        ('Additional', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(RecyclerMaterial)
class RecyclerMaterialAdmin(admin.ModelAdmin):
    list_display = ['recycler', 'material', 'price_per_kg', 'is_active']
    list_filter = ['is_active', 'recycler', 'material']
    search_fields = ['recycler__recycler_name', 'material__material_name']
    list_editable = ['price_per_kg', 'is_active']


# @admin.register(VendorAssignment)
# class VendorAssignmentAdmin(admin.ModelAdmin):
#     list_display = ['vendor', 'school', 'material', 'contract_start', 'contract_end', 'is_active']
#     list_filter = ['is_active', 'vendor', 'school', 'material']
#     search_fields = ['vendor__recycler_name', 'school__school_name']
#     list_editable = ['is_active']