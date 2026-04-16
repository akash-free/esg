from decimal import Decimal
from .models import EmissionFactor

def calculate_waste_impact(waste_category, treatment_method, weight_kg):
    """
    Waste entry ke liye CO₂e, Water, Trees calculate karta hai
    Returns: (co2e_kg, water_saved_litres, trees_equivalent, factor_used)
    """
    try:
        factor = EmissionFactor.objects.get(
            waste_category=waste_category,
            treatment_method=treatment_method
        )
    except EmissionFactor.DoesNotExist:
        # Agar factor nahi mila to default values
        return (Decimal('0'), Decimal('0'), Decimal('0'), Decimal('0'))
    
    weight_tonnes = Decimal(str(weight_kg)) / Decimal('1000')
    
    # CO₂e calculation (kg me)
    co2e_kg = weight_kg * abs(factor.factor_value)
    
    # Water saved calculation (litres)
    water_saved = Decimal('0')
    if factor.water_factor:
        water_saved = weight_tonnes * factor.water_factor
    
    # Trees equivalent (sirf paper category ke liye)
    trees = Decimal('0')
    if 'paper' in waste_category.lower() and factor.trees_factor:
        trees = weight_tonnes * factor.trees_factor
    
    return (co2e_kg, water_saved, trees, factor.factor_value)