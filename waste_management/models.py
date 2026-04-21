from django.db import models
from schools.models import ReportingYear

class WasteEntry(models.Model):
    """
    Har waste entry ka record — ye table se dashboard ke saare numbers aayenge
    Total Waste, Diverted, CO₂e, Water, Trees — sab yahan se calculate hoga
    """
    SOURCE_CHOICES = [
        ('classroom', 'Classroom'),
        ('office', 'Office'),
        ('event', 'Event'),
        ('other', 'Other'),
    ]
    
    TREATMENT_CHOICES = [
        ('recycled', 'Recycled'),
        ('composted', 'Composted'),
        ('landfilled', 'Landfilled'),
        ('incinerated', 'Incinerated'),
        ('co_processed', 'Co-processed'),
    ]
    
    # Ye fields user fill karega
    reporting_year = models.ForeignKey(ReportingYear, on_delete=models.CASCADE, related_name='waste_entries')
    entry_date = models.DateField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='classroom')
    waste_category = models.CharField(max_length=100)  # Paper & Cardboard, Plastics, Organic, etc.
    weight_kg = models.DecimalField(max_digits=10, decimal_places=3)  # weight in kg
    treatment_method = models.CharField(max_length=20, choices=TREATMENT_CHOICES)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)  # optional
    
    # Ye fields auto-calculate honge (snapshot at entry time)
    emission_factor_used = models.DecimalField(max_digits=10, decimal_places=6, default=0)
    co2e_kg = models.DecimalField(max_digits=12, decimal_places=4, default=0)  # CO₂e in kg
    water_saved_litres = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    trees_equivalent = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    notes = models.TextField(blank=True, null=True, help_text="Additional notes about the waste entry")
    teacher = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='waste_entries'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'waste_entries'
        ordering = ['-entry_date']
        verbose_name = 'Waste Entry'
        verbose_name_plural = 'Waste Entries'
    
    def __str__(self):
        return f"{self.entry_date} - {self.waste_category}: {self.weight_kg}kg"
    
    remaining_weight = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            if not self.remaining_weight:
                self.remaining_weight = self.weight_kg
        super().save(*args, **kwargs)



class WasteDispatch(models.Model):
    """Track waste dispatched to vendors"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('dispatched', 'Dispatched'),
        ('collected', 'Collected'),
        ('completed', 'Completed'),
    ]
    
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    vendor = models.ForeignKey('recycler_management.Recycler', on_delete=models.CASCADE)
    principal = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    
    
    dispatch_date = models.DateField(auto_now_add=True)
    scheduled_pickup = models.DateField(null=True, blank=True)
    
    total_weight = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'waste_dispatches'
        ordering = ['-created_at']


class WasteDispatchItem(models.Model):
    """Which waste entries were dispatched"""
    
    dispatch = models.ForeignKey(WasteDispatch, on_delete=models.CASCADE, related_name='items')

    waste_entry = models.ForeignKey('WasteEntry', on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=10, decimal_places=3)
    
    class Meta:
        db_table = 'waste_dispatch_items'