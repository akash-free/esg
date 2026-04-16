# # =============================================================================
# # FILE    : recycler_management/models.py
# # PURPOSE : Material master list, Recycler profile, Recycler-Material mapping
# # =============================================================================

# import logging
# from django.db import models

# logger = logging.getLogger(__name__)


# # =============================================================================
# # MATERIAL MODEL — master waste type list
# # =============================================================================
# class Material(models.Model):

#     material_name = models.CharField(max_length=100, unique=True)
#     unit          = models.CharField(max_length=10, default='kg')
#     description   = models.TextField(blank=True, null=True)
#     is_active     = models.BooleanField(default=True)

#     class Meta:
#         db_table = 'materials'
#         ordering = ['material_name']

#     def __str__(self):
#         return f"{self.material_name} ({self.unit})"


# # =============================================================================
# # RECYCLER MODEL
# # =============================================================================
# class Recycler(models.Model):

#     class StatusChoices(models.TextChoices):
#         ACTIVE   = 'active',   'Active'
#         INACTIVE = 'inactive', 'Inactive'
#         PENDING  = 'pending',  'Pending Approval'

#     recycler_name  = models.CharField(max_length=255)
#     address        = models.TextField()
#     city           = models.CharField(max_length=100)
#     contact_email  = models.EmailField(blank=True, null=True)
#     contact_phone  = models.CharField(max_length=20, blank=True, null=True)
#     trust_score    = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
#     status         = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
#     created_at     = models.DateTimeField(auto_now_add=True)
#     updated_at     = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'recyclers'
#         ordering = ['recycler_name']

#     def __str__(self):
#         return f"{self.recycler_name} - {self.city}"


# # =============================================================================
# # RECYCLER MATERIAL — which recycler accepts which material
# # =============================================================================
# class RecyclerMaterial(models.Model):

#     recycler = models.ForeignKey(Recycler, on_delete=models.CASCADE, related_name='accepted_materials')
#     material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='recycler_assignments')

#     class Meta:
#         db_table        = 'recycler_materials'
#         unique_together = ('recycler', 'material')

#     def __str__(self):
#         return f"{self.recycler.recycler_name} accepts {self.material.material_name}"

# =============================================================================
# FILE    : recycler_management/models.py
# PURPOSE : Material master list, Recycler profile, Recycler-Material mapping
#           Vendor Assignment for schools
# =============================================================================

import logging
from django.db import models

logger = logging.getLogger(__name__)


# =============================================================================
# MATERIAL MODEL — master waste type list
# =============================================================================
class Material(models.Model):
    """Waste material categories like Paper, Plastic, etc."""

    material_name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(max_length=10, default='kg')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'materials'
        ordering = ['material_name']

    def __str__(self):
        return f"{self.material_name} ({self.unit})"


# =============================================================================
# RECYCLER/VENDOR MODEL — Upgraded with all vendor fields
# =============================================================================
class Recycler(models.Model):
    """Recycler/Vendor profile — waste collection and processing partner"""

    # Status choices
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending Approval'

    # Vendor type choices
    class VendorTypeChoices(models.TextChoices):
        COLLECTION = 'collection', 'Collection Vendor'
        RECYCLING = 'recycling', 'Recycling Vendor'
        DISPOSAL = 'disposal', 'Disposal Vendor'
        COMPOSTING = 'composting', 'Composting Vendor'
        E_WASTE = 'e_waste', 'E-waste Vendor'

    # ========== BASIC INFO ==========
    recycler_name = models.CharField(max_length=255, help_text="Vendor/Recycler company name")
    vendor_type = models.CharField(
        max_length=100, 
        choices=VendorTypeChoices.choices, 
        default=VendorTypeChoices.RECYCLING,
        help_text="Type of vendor services"
    )

    # ========== ADDRESS & CONTACT ==========
    address = models.TextField(help_text="Full address")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True, help_text="Primary contact person name")
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    # ========== BUSINESS INFO ==========
    gst_number = models.CharField(max_length=20, blank=True, null=True, help_text="GST registration number")
    certifications = models.TextField(blank=True, null=True, help_text="ISO, environmental certifications")

    # ========== OPERATIONAL INFO ==========
    processing_capacity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Daily processing capacity in kg"
    )
    recycling_efficiency = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        help_text="Recycling efficiency percentage"
    )
    minimum_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Minimum pickup quantity in kg"
    )
    pickup_schedule = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Pickup days: Monday, Wednesday, Friday"
    )
    service_cities = models.TextField(
        blank=True, null=True,
        help_text="Cities where vendor provides service (comma separated)"
    )

    # ========== PERFORMANCE METRICS ==========
    trust_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        help_text="Trust score based on performance (0-100)"
    )
    total_collected = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Total waste collected in kg"
    )
    total_processed = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Total waste processed in kg"
    )
    certificates_issued = models.IntegerField(default=0, help_text="Number of recycling certificates issued")

    # ========== STATUS & NOTES ==========
    status = models.CharField(
        max_length=10, 
        choices=StatusChoices.choices, 
        default=StatusChoices.PENDING
    )
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about vendor")

    # ========== TIMESTAMPS ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'recyclers'
        ordering = ['recycler_name']

    def __str__(self):
        return f"{self.recycler_name} - {self.city}"


# =============================================================================
# RECYCLER MATERIAL — which recycler accepts which material
# =============================================================================
class RecyclerMaterial(models.Model):
    """Mapping of which materials a recycler accepts"""

    recycler = models.ForeignKey(
        Recycler, 
        on_delete=models.CASCADE, 
        related_name='accepted_materials'
    )
    material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='recycler_assignments'
    )
    price_per_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        help_text="Price offered per kg (if applicable)"
    )
    is_active = models.BooleanField(default=True, help_text="Whether this material is currently accepted")

    class Meta:
        db_table = 'recycler_materials'
        unique_together = ('recycler', 'material')

    def __str__(self):
        return f"{self.recycler.recycler_name} → {self.material.material_name} (₹{self.price_per_kg}/kg)"


# =============================================================================
# VENDOR ASSIGNMENT — Vendor assigned to school for specific material
# =============================================================================
class VendorAssignment(models.Model):
    """Which vendor is assigned to which school for which material in a reporting year"""

    vendor = models.ForeignKey(
        Recycler, 
        on_delete=models.CASCADE, 
        related_name='school_assignments'
    )
    school = models.ForeignKey(
        'schools.School', 
        on_delete=models.CASCADE, 
        related_name='vendor_assignments'
    )
    reporting_year = models.ForeignKey(
        'schools.ReportingYear', 
        on_delete=models.CASCADE, 
        related_name='vendor_assignments'
    )
    material = models.ForeignKey(
        Material, 
        on_delete=models.CASCADE, 
        related_name='vendor_assignments'
    )
    contract_start = models.DateField(help_text="Contract start date")
    contract_end = models.DateField(null=True, blank=True, help_text="Contract end date (optional)")
    is_active = models.BooleanField(default=True, help_text="Whether this assignment is currently active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vendor_assignments'
        unique_together = ('vendor', 'school', 'reporting_year', 'material')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.vendor.recycler_name} → {self.school.school_name} ({self.material.material_name})"