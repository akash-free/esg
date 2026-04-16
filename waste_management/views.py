
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WasteEntry
from esg_tracking.models import WasteCategory, WasteSubCategory, TreatmentMethod, ESGFactor
from decimal import Decimal

# @login_required
# def waste_entry_add(request):
#     """Add waste entry — dynamic from database"""
    
#     if request.user.role != 'teacher':
#         messages.error(request, 'Access denied.')
#         return redirect('login')
    
#     categories = WasteCategory.objects.filter(is_active=True)
#     treatments = TreatmentMethod.objects.filter(is_active=True)
    
#     if request.method == 'POST':
#         # Get form data
#         category_id = request.POST.get('category_id')
#         sub_category_id = request.POST.get('sub_category_id')
#         treatment_id = request.POST.get('treatment_id')
#         weight_kg = request.POST.get('weight_kg')
#         entry_date = request.POST.get('entry_date')
#         source = request.POST.get('source')
#         notes = request.POST.get('notes')
        
#         # ========== VALIDATION ==========
#         # Check required fields
#         if not category_id:
#             messages.error(request, 'Please select a waste category.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         if not treatment_id:
#             messages.error(request, 'Please select a treatment method.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         if not weight_kg:
#             messages.error(request, 'Please enter weight.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         # Convert to integers (only if not empty)
#         try:
#             category_id = int(category_id)
#             treatment_id = int(treatment_id)
            
#             # Sub-category is optional
#             if sub_category_id and sub_category_id.strip():
#                 sub_category_id = int(sub_category_id)
#             else:
#                 sub_category_id = None
                
#         except ValueError:
#             messages.error(request, 'Invalid input values.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         weight_kg = float(weight_kg)
#         # =================================
        
#         # Get category and treatment names
#         category = WasteCategory.objects.get(id=category_id)
#         treatment = TreatmentMethod.objects.get(id=treatment_id)
        
#         # Get sub-category name if selected
#         sub_category = None
#         if sub_category_id:
#             sub_category = WasteSubCategory.objects.get(id=sub_category_id)
        
#         # Get ESG factor (only if sub-category selected)
#         esg_factor = None
#         if sub_category_id:
#             esg_factor = ESGFactor.objects.filter(
#                 sub_category_id=sub_category_id,
#                 treatment_id=treatment_id
#             ).first()
        
#         # Calculate impacts
#         if esg_factor:
#             co2e_kg = weight_kg * abs(float(esg_factor.co2_factor))
#             water_saved = (weight_kg / 1000) * float(esg_factor.water_factor or 0)
#             trees_saved = (weight_kg / 1000) * float(esg_factor.trees_factor or 0)
#             emission_factor = float(esg_factor.co2_factor)
#         else:
#             # Default calculation based on category
#             if category.name.lower() in ['paper & cardboard', 'paper']:
#                 co2e_kg = weight_kg * 0.82
#                 water_saved = (weight_kg / 1000) * 26500
#                 trees_saved = (weight_kg / 1000) * 24
#             elif category.name.lower() in ['plastics', 'plastic']:
#                 co2e_kg = weight_kg * 1.54
#                 water_saved = 0
#                 trees_saved = 0
#             else:
#                 co2e_kg = weight_kg * 0.5
#                 water_saved = 0
#                 trees_saved = 0
#             emission_factor = co2e_kg / weight_kg if weight_kg > 0 else 0
        
#         from schools.models import ReportingYear
#         reporting_year = ReportingYear.objects.filter(status='active').first()
        
#         if not reporting_year:
#             messages.error(request, 'No active reporting year found.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         # Save entry
#         WasteEntry.objects.create(
#             reporting_year=reporting_year,
#             entry_date=entry_date,
#             source=source,
#             waste_category=category.name,
#             weight_kg=weight_kg,
#             treatment_method=treatment.name,
#             vendor_name=request.POST.get('vendor_name', ''),
#             emission_factor_used=emission_factor,
#             co2e_kg=co2e_kg,
#             water_saved_litres=water_saved,
#             trees_equivalent=trees_saved,
#             notes=notes,
#             teacher=request.user,
#         )
        
#         messages.success(request, f'Waste entry of {weight_kg} kg added!')
#         return redirect('waste_entry_list')
    
#     context = {
#         'categories': categories,
#         'treatments': treatments,
#     }
#     return render(request, 'waste_management/entry_form.html', context)

# @login_required
# def waste_entry_add(request):
#     """Add waste entry — dynamic from database"""
#     print("=" * 50)
#     print("DEBUG: waste_entry_add CALLED")
#     print(f"User: {request.user}")
#     print(f"User role: {request.user.role}")
#     print(f"User school_name: {request.user.school_name}")
#     print("=" * 50)
    
#     if request.user.role != 'teacher':
#         print("DEBUG: Role check FAILED - redirecting to login")
#         messages.error(request, 'Access denied.')
#         return redirect('login')
    
#     teacher = request.user
#     teacher_school_name = teacher.school_name
#     teacher_short_name = teacher.school_short_name

#     print(f"DEBUG: teacher_school_name: {teacher_school_name}")
#     print(f"DEBUG: teacher_short_name: {teacher_short_name}")

#     if not teacher_short_name and not teacher_school_name:
#         messages.error(request, 'School not linked to your account. Contact admin.')
#         return redirect('teacher_dashboard')

#     from schools.models import School, ReportingYear

#     # Try to find by short_name first (more reliable)
#     school = None
#     if teacher_short_name:
#         school = School.objects.filter(short_name=teacher_short_name).first()
#         print(f"DEBUG: Search by short_name '{teacher_short_name}' -> {school}")

#     # If not found, try by school_name
#     if not school and teacher_school_name:
#         school = School.objects.filter(school_name=teacher_school_name).first()
#         print(f"DEBUG: Search by school_name '{teacher_school_name}' -> {school}")

#     if not school:
#         messages.error(request, f'School not found. Please contact admin.')
#         return redirect('teacher_dashboard')
    
#     # Get active reporting year for this school
#     reporting_year = ReportingYear.objects.filter(
#         school=school, 
#         status='active'
#     ).first()
    
#     if not reporting_year:
#         messages.error(request, f'No active reporting year for {school.school_name}')
#         return redirect('teacher_dashboard')
#     # =========================================
    
#     categories = WasteCategory.objects.filter(is_active=True)
#     treatments = TreatmentMethod.objects.filter(is_active=True)
    
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         sub_category_id = request.POST.get('sub_category_id')
#         treatment_id = request.POST.get('treatment_id')
#         weight_kg = request.POST.get('weight_kg')
#         entry_date = request.POST.get('entry_date')
#         source = request.POST.get('source')
#         notes = request.POST.get('notes')
        
#         # Validation
#         if not category_id:
#             messages.error(request, 'Please select a waste category.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         if not treatment_id:
#             messages.error(request, 'Please select a treatment method.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         if not weight_kg:
#             messages.error(request, 'Please enter weight.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         try:
#             category_id = int(category_id)
#             treatment_id = int(treatment_id)
#             if sub_category_id and sub_category_id.strip():
#                 sub_category_id = int(sub_category_id)
#             else:
#                 sub_category_id = None
#         except ValueError:
#             messages.error(request, 'Invalid input values.')
#             return render(request, 'waste_management/entry_form.html', {
#                 'categories': categories,
#                 'treatments': treatments
#             })
        
#         weight_kg = float(weight_kg)
        
#         category = WasteCategory.objects.get(id=category_id)
#         treatment = TreatmentMethod.objects.get(id=treatment_id)
        
#         sub_category = None
#         if sub_category_id:
#             sub_category = WasteSubCategory.objects.get(id=sub_category_id)
        
#         esg_factor = None
#         if sub_category_id:
#             esg_factor = ESGFactor.objects.filter(
#                 sub_category_id=sub_category_id,
#                 treatment_id=treatment_id
#             ).first()
        
#         if esg_factor:
#             co2e_kg = weight_kg * abs(float(esg_factor.co2_factor))
#             water_saved = (weight_kg / 1000) * float(esg_factor.water_factor or 0)
#             trees_saved = (weight_kg / 1000) * float(esg_factor.trees_factor or 0)
#             emission_factor = float(esg_factor.co2_factor)
#         else:
#             if category.name.lower() in ['paper & cardboard', 'paper']:
#                 co2e_kg = weight_kg * 0.82
#                 water_saved = (weight_kg / 1000) * 26500
#                 trees_saved = (weight_kg / 1000) * 24
#             elif category.name.lower() in ['plastics', 'plastic']:
#                 co2e_kg = weight_kg * 1.54
#                 water_saved = 0
#                 trees_saved = 0
#             else:
#                 co2e_kg = weight_kg * 0.5
#                 water_saved = 0
#                 trees_saved = 0
#             emission_factor = co2e_kg / weight_kg if weight_kg > 0 else 0
        
#         # Save entry with teacher's reporting year
#         WasteEntry.objects.create(
#             reporting_year=reporting_year,  # ← Teacher's school ka reporting year
#             entry_date=entry_date,
#             source=source,
#             waste_category=category.name,
#             weight_kg=weight_kg,
#             treatment_method=treatment.name,
#             vendor_name=request.POST.get('vendor_name', ''),
#             emission_factor_used=emission_factor,
#             co2e_kg=co2e_kg,
#             water_saved_litres=water_saved,
#             trees_equivalent=trees_saved,
#             notes=notes,
#             teacher=request.user,
#         )
        
#         messages.success(request, f'Waste entry of {weight_kg} kg added!')
#         return redirect('waste_entry_list')
    
#     context = {
#         'categories': categories,
#         'treatments': treatments,
#     }
#     return render(request, 'waste_management/entry_form.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WasteEntry
from esg_tracking.models import WasteCategory, WasteSubCategory, TreatmentMethod, ESGFactor
from decimal import Decimal

@login_required
def waste_entry_add(request):
    """Add waste entry — simple form for teachers"""
    print("=" * 50)
    print("DEBUG: waste_entry_add CALLED")
    print(f"User: {request.user}")
    print(f"User role: {request.user.role}")
    print("=" * 50)
    
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    # ========== GET TEACHER'S SCHOOL ==========
    teacher = request.user
    teacher_short_name = teacher.school_short_name

    if not teacher_short_name and not teacher.school_name:
        messages.error(request, 'School not linked to your account. Contact admin.')
        return redirect('teacher_dashboard')

    from schools.models import School, ReportingYear

    school = None
    if teacher_short_name:
        school = School.objects.filter(short_name=teacher_short_name).first()
    if not school and teacher.school_name:
        school = School.objects.filter(school_name=teacher.school_name).first()

    if not school:
        messages.error(request, f'School not found. Please contact admin.')
        return redirect('teacher_dashboard')
    
    # Get active reporting year for this school
    reporting_year = ReportingYear.objects.filter(school=school, status='active').first()
    
    if not reporting_year:
        messages.error(request, f'No active reporting year for {school.school_name}')
        return redirect('teacher_dashboard')
    # =========================================
    
    categories = WasteCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        weight_kg = request.POST.get('weight_kg')
        entry_date = request.POST.get('entry_date')
        source = request.POST.get('source')
        notes = request.POST.get('notes')
        
        # Validation
        if not category_id:
            messages.error(request, 'Please select a waste category.')
            return render(request, 'waste_management/entry_form.html', {
                'categories': categories
            })
        
        if not weight_kg:
            messages.error(request, 'Please enter weight.')
            return render(request, 'waste_management/entry_form.html', {
                'categories': categories
            })
        
        try:
            category_id = int(category_id)
            weight_kg = float(weight_kg)
        except ValueError:
            messages.error(request, 'Invalid input values.')
            return render(request, 'waste_management/entry_form.html', {
                'categories': categories
            })
        
        # Get category
        category = WasteCategory.objects.get(id=category_id)
        
        # ========== AUTO: Get default sub-category and treatment ==========
        # Try to get default from category, otherwise take first available
        sub_category = category.default_sub_category
        if not sub_category:
            sub_category = WasteSubCategory.objects.filter(category=category, is_active=True).first()
        
        treatment = category.default_treatment
        if not treatment:
            treatment = TreatmentMethod.objects.filter(is_active=True).first()
        
        sub_category_id = sub_category.id if sub_category else None
        treatment_id = treatment.id if treatment else None
        
        # Fetch ESG factor
        esg_factor = None
        if sub_category_id and treatment_id:
            esg_factor = ESGFactor.objects.filter(
                sub_category_id=sub_category_id,
                treatment_id=treatment_id
            ).first()
        # ================================================================
        
        # Calculate impacts
        if esg_factor:
            co2e_kg = weight_kg * abs(float(esg_factor.co2_factor))
            water_saved = (weight_kg / 1000) * float(esg_factor.water_factor or 0)
            trees_saved = (weight_kg / 1000) * float(esg_factor.trees_factor or 0)
            emission_factor = float(esg_factor.co2_factor)
        else:
            # Fallback calculation
            if category.name.lower() in ['paper & cardboard', 'paper']:
                co2e_kg = weight_kg * 0.82
                water_saved = (weight_kg / 1000) * 26500
                trees_saved = (weight_kg / 1000) * 24
            elif category.name.lower() in ['plastics', 'plastic']:
                co2e_kg = weight_kg * 1.54
                water_saved = 0
                trees_saved = 0
            else:
                co2e_kg = weight_kg * 0.5
                water_saved = 0
                trees_saved = 0
            emission_factor = co2e_kg / weight_kg if weight_kg > 0 else 0
        
        # Save entry
        WasteEntry.objects.create(
            reporting_year=reporting_year,
            entry_date=entry_date,
            source=source,
            waste_category=category.name,
            weight_kg=weight_kg,
            treatment_method=treatment.name if treatment else 'Recycled',
            vendor_name=request.POST.get('vendor_name', ''),
            emission_factor_used=emission_factor,
            co2e_kg=co2e_kg,
            water_saved_litres=water_saved,
            trees_equivalent=trees_saved,
            notes=notes,
            teacher=request.user,
        )
        
        messages.success(request, f'Waste entry of {weight_kg} kg added!')
        return redirect('waste_entry_list')
    
    context = {
        'categories': categories,
    }
    return render(request, 'waste_management/entry_form.html', context)

@login_required
def waste_entry_list(request):
    """List waste entries"""
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    # entries = WasteEntry.objects.all().order_by('-entry_date')
    entries = WasteEntry.objects.filter(teacher=request.user).order_by('-entry_date')
    return render(request, 'waste_management/entry_list.html', {'entries': entries})


# ========== EDIT WASTE ENTRY ==========
@login_required
def waste_entry_edit(request, id):
    """Edit waste entry"""
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    entry = get_object_or_404(WasteEntry, id=id)
    
    if request.method == 'POST':
        entry.waste_category = request.POST.get('waste_category')
        entry.weight_kg = request.POST.get('weight_kg')
        entry.entry_date = request.POST.get('entry_date')
        
        # Recalculate CO₂
        entry.co2e_kg = float(entry.weight_kg) * 0.82
        
        entry.save()
        
        messages.success(request, 'Waste entry updated successfully!')
        return redirect('waste_entry_list')
    
    context = {
        'entry': entry,
        'categories': ['Paper & Cardboard', 'Plastics', 'Organic', 'Metal', 'Glass', 'E-waste']
    }
    return render(request, 'waste_management/entry_edit.html', context)


# ========== DELETE WASTE ENTRY ==========
@login_required
def waste_entry_delete(request, id):
    """Delete waste entry"""
    if request.user.role != 'teacher':
        messages.error(request, 'Access denied.')
        return redirect('login')
    
    entry = get_object_or_404(WasteEntry, id=id)
    
    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Waste entry deleted successfully!')
        return redirect('waste_entry_list')
    
    return render(request, 'waste_management/entry_confirm_delete.html', {'entry': entry})