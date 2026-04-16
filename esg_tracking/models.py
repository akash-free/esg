from django.db import models

class EmissionFactor(models.Model):
    """
    Ye table store karegi ki har waste category ka emission factor kya hai
    Jaise: Paper Recycled karne se -0.82 t CO₂e/tonne bachta hai
    """
    waste_category = models.CharField(max_length=100)  # Paper & Cardboard, Plastics, etc.
    treatment_method = models.CharField(max_length=50)  # recycled, composted, etc.
    factor_value = models.DecimalField(max_digits=10, decimal_places=6)  # CO₂e factor
    water_factor = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  # litres saved per tonne
    trees_factor = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # trees per tonne
    
    class Meta:
        db_table = 'emission_factors'
        verbose_name = 'Emission Factor'
        verbose_name_plural = 'Emission Factors'
    
    def __str__(self):
        return f"{self.waste_category} - {self.treatment_method}: {self.factor_value}"
    

from django.db import models

# ============================================================================
# LEVEL 1: WASTE CATEGORY (Main Category)
# ============================================================================
# class WasteCategory(models.Model):
#     """Main waste categories like Paper & Cardboard, Plastics, Organic, etc."""
    
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True, null=True)
#     icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class")
#     order = models.IntegerField(default=0, help_text="Display order")
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     class Meta:
#         db_table = 'esg_waste_categories'
#         ordering = ['order', 'name']
#         verbose_name = 'Waste Category'
#         verbose_name_plural = 'Waste Categories'
    
#     def __str__(self):
#         return self.name

class WasteCategory(models.Model):
    """Main waste categories like Paper & Cardboard, Plastics, Organic, etc."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="Font Awesome icon class")
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ========== ADD THESE FIELDS ==========
    default_sub_category = models.ForeignKey(
        'WasteSubCategory', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='default_for_categories'
    )
    default_treatment = models.ForeignKey(
        'TreatmentMethod', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='default_for_categories'
    )
    # =====================================
    
    class Meta:
        db_table = 'esg_waste_categories'
        ordering = ['order', 'name']
        verbose_name = 'Waste Category'
        verbose_name_plural = 'Waste Categories'
    
    def __str__(self):
        return self.name

# ============================================================================
# LEVEL 2: WASTE SUB-CATEGORY (Detailed types)
# ============================================================================
class WasteSubCategory(models.Model):
    """Detailed sub-categories like Virgin Paper (Pine), Recycled Paper, etc."""
    
    # Tree type choices for Paper category
    TREE_TYPE_CHOICES = [
        ('pine', 'Pine (Softwood)'),
        ('spruce', 'Spruce (Softwood)'),
        ('eucalyptus', 'Eucalyptus (Hardwood)'),
        ('acacia', 'Acacia (Hardwood)'),
        ('mixed', 'Mixed (Softwood + Hardwood)'),
        ('bamboo', 'Bamboo (Grass)'),
        ('hemp', 'Hemp (Crop)'),
        ('bagasse', 'Bagasse (Agricultural Waste)'),
        ('cotton', 'Cotton (Textile Waste)'),
        ('none', 'None (Recycled/Alternative)'),
        ('other', 'Other'),
    ]
    
    category = models.ForeignKey(WasteCategory, on_delete=models.CASCADE, related_name='sub_categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    # Paper specific fields (optional for other categories)
    tree_type = models.CharField(max_length=50, choices=TREE_TYPE_CHOICES, blank=True, null=True)
    growth_rate_years = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., '20-30 years'")
    co2_absorption = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="kg CO₂ per tree per year")
    
    # Common fields
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'esg_waste_sub_categories'
        ordering = ['order', 'name']
        unique_together = ['category', 'name']
        verbose_name = 'Waste Sub-Category'
        verbose_name_plural = 'Waste Sub-Categories'
    
    def __str__(self):
        return f"{self.category.name} → {self.name}"


# ============================================================================
# LEVEL 3: TREATMENT METHOD
# ============================================================================
class TreatmentMethod(models.Model):
    """Treatment methods like Recycled, Composted, Landfilled, Incinerated, etc."""
    
    CO2_EFFECT_CHOICES = [
        ('negative', 'Negative (Avoids CO₂)'),
        ('positive', 'Positive (Generates CO₂)'),
        ('neutral', 'Neutral'),
    ]
    
    WATER_EFFECT_CHOICES = [
        ('positive', 'Positive (Saves Water)'),
        ('negative', 'Negative (Consumes Water)'),
        ('neutral', 'Neutral'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    co2_effect = models.CharField(max_length=20, choices=CO2_EFFECT_CHOICES, default='neutral')
    water_effect = models.CharField(max_length=20, choices=WATER_EFFECT_CHOICES, default='neutral')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'esg_treatment_methods'
        ordering = ['order', 'name']
        verbose_name = 'Treatment Method'
        verbose_name_plural = 'Treatment Methods'
    
    def __str__(self):
        return self.name


# ============================================================================
# LEVEL 4: ESG FACTOR (Impact Factors)
# ============================================================================
class ESGFactor(models.Model):
    """ESG impact factors for each sub-category and treatment combination."""
    
    sub_category = models.ForeignKey(WasteSubCategory, on_delete=models.CASCADE, related_name='esg_factors')
    treatment = models.ForeignKey(TreatmentMethod, on_delete=models.CASCADE, related_name='esg_factors')
    
    # Impact Factors
    co2_factor = models.DecimalField(
        max_digits=10, decimal_places=6, 
        help_text="t CO₂e per tonne (negative = avoided, positive = generated)"
    )
    water_factor = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True,
        help_text="Litres saved per tonne"
    )
    trees_factor = models.DecimalField(
        max_digits=10, decimal_places=4, null=True, blank=True,
        help_text="Trees saved per tonne (only for paper category)"
    )
    energy_factor = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="kWh saved per tonne"
    )
    
    # Source Information
    source_standard = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., IPCC 2019, GHG Protocol")
    notes = models.TextField(blank=True, null=True)
    
    # Audit
    last_edited_by = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'esg_factors'
        unique_together = ['sub_category', 'treatment']
        ordering = ['sub_category__category__order', 'sub_category__order', 'treatment__order']
        verbose_name = 'ESG Factor'
        verbose_name_plural = 'ESG Factors'
    
    def __str__(self):
        return f"{self.sub_category.category.name} → {self.sub_category.name} → {self.treatment.name}: {self.co2_factor}"
    
    def get_co2_kg(self, weight_kg):
        """Calculate CO₂ in kg for given weight in kg"""
        return float(weight_kg) * abs(float(self.co2_factor))
    
    def get_water_litres(self, weight_kg):
        """Calculate water saved in litres for given weight in kg"""
        if self.water_factor:
            return (float(weight_kg) / 1000) * float(self.water_factor)
        return 0
    
    def get_trees(self, weight_kg):
        """Calculate trees saved for given weight in kg"""
        if self.trees_factor:
            return (float(weight_kg) / 1000) * float(self.trees_factor)
        return 0