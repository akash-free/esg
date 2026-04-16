from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WasteCategory, WasteSubCategory, TreatmentMethod, ESGFactor


# ========== WASTE CATEGORY CRUD ==========

@login_required
def category_list(request):
    """List all waste categories"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    categories = WasteCategory.objects.all()
    return render(request, 'esg_tracking/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    """Create new waste category"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        icon = request.POST.get('icon')
        order = request.POST.get('order', 0)
        
        if WasteCategory.objects.filter(name=name).exists():
            messages.error(request, f'Category "{name}" already exists!')
        else:
            WasteCategory.objects.create(
                name=name,
                description=description,
                icon=icon,
                order=order,
                is_active=True
            )
            messages.success(request, f'Category "{name}" created!')
            return redirect('esg_category_list')
    
    return render(request, 'esg_tracking/category_form.html')


@login_required
def category_edit(request, id):
    """Edit waste category"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        
        return redirect('superadmin_dashboard')
    
    category = get_object_or_404(WasteCategory, id=id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.icon = request.POST.get('icon')
        category.order = request.POST.get('order', 0)
        category.is_active = request.POST.get('is_active') == 'on'
        category.save()
        messages.success(request, f'Category "{category.name}" updated!')
        return redirect('esg_category_list')
    
    return render(request, 'esg_tracking/category_form.html', {'category': category})


@login_required
def category_delete(request, id):
    """Delete waste category"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    category = get_object_or_404(WasteCategory, id=id)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted!')
        return redirect('esg_category_list')
    
    return render(request, 'esg_tracking/category_confirm_delete.html', {'category': category})


# ========== SUB-CATEGORY CRUD ==========

@login_required
def subcategory_list(request):
    """List all sub-categories"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    subcategories = WasteSubCategory.objects.select_related('category').all()
    return render(request, 'esg_tracking/subcategory_list.html', {'subcategories': subcategories})


@login_required
def subcategory_create(request):
    """Create new sub-category"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    categories = WasteCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        name = request.POST.get('name')
        description = request.POST.get('description')
        tree_type = request.POST.get('tree_type')
        growth_rate = request.POST.get('growth_rate_years')
        co2_absorption = request.POST.get('co2_absorption')
        order = request.POST.get('order', 0)
        
        category = get_object_or_404(WasteCategory, id=category_id)
        
        if WasteSubCategory.objects.filter(category=category, name=name).exists():
            messages.error(request, f'Sub-category "{name}" already exists in this category!')
        else:
            WasteSubCategory.objects.create(
                category=category,
                name=name,
                description=description,
                tree_type=tree_type,
                growth_rate_years=growth_rate,
                co2_absorption=co2_absorption,
                order=order,
                is_active=True
            )
            messages.success(request, f'Sub-category "{name}" created!')
            return redirect('esg_subcategory_list')
    
    return render(request, 'esg_tracking/subcategory_form.html', {'categories': categories})


@login_required
def subcategory_edit(request, id):
    """Edit sub-category"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    subcategory = get_object_or_404(WasteSubCategory, id=id)
    categories = WasteCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        subcategory.category_id = request.POST.get('category')
        subcategory.name = request.POST.get('name')
        subcategory.description = request.POST.get('description')
        subcategory.tree_type = request.POST.get('tree_type')
        subcategory.growth_rate_years = request.POST.get('growth_rate_years')
        subcategory.co2_absorption = request.POST.get('co2_absorption')
        subcategory.order = request.POST.get('order', 0)
        subcategory.is_active = request.POST.get('is_active') == 'on'
        subcategory.save()
        messages.success(request, f'Sub-category "{subcategory.name}" updated!')
        return redirect('esg_subcategory_list')
    
    return render(request, 'esg_tracking/subcategory_form.html', {
        'subcategory': subcategory,
        'categories': categories
    })


@login_required
def subcategory_delete(request, id):
    """Delete sub-category"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    subcategory = get_object_or_404(WasteSubCategory, id=id)
    
    if request.method == 'POST':
        subcategory_name = subcategory.name
        subcategory.delete()
        messages.success(request, f'Sub-category "{subcategory_name}" deleted!')
        return redirect('esg_subcategory_list')
    
    return render(request, 'esg_tracking/subcategory_confirm_delete.html', {'subcategory': subcategory})


# ========== TREATMENT METHOD CRUD ==========

@login_required
def treatment_list(request):
    """List all treatment methods"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    treatments = TreatmentMethod.objects.all()
    return render(request, 'esg_tracking/treatment_list.html', {'treatments': treatments})


@login_required
def treatment_create(request):
    """Create new treatment method"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        co2_effect = request.POST.get('co2_effect')
        water_effect = request.POST.get('water_effect')
        order = request.POST.get('order', 0)
        
        if TreatmentMethod.objects.filter(name=name).exists():
            messages.error(request, f'Treatment "{name}" already exists!')
        else:
            TreatmentMethod.objects.create(
                name=name,
                description=description,
                co2_effect=co2_effect,
                water_effect=water_effect,
                order=order,
                is_active=True
            )
            messages.success(request, f'Treatment "{name}" created!')
            return redirect('esg_treatment_list')
    
    return render(request, 'esg_tracking/treatment_form.html')


@login_required
def treatment_edit(request, id):
    """Edit treatment method"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    treatment = get_object_or_404(TreatmentMethod, id=id)
    
    if request.method == 'POST':
        treatment.name = request.POST.get('name')
        treatment.description = request.POST.get('description')
        treatment.co2_effect = request.POST.get('co2_effect')
        treatment.water_effect = request.POST.get('water_effect')
        treatment.order = request.POST.get('order', 0)
        treatment.is_active = request.POST.get('is_active') == 'on'
        treatment.save()
        messages.success(request, f'Treatment "{treatment.name}" updated!')
        return redirect('esg_treatment_list')
    
    return render(request, 'esg_tracking/treatment_form.html', {'treatment': treatment})


@login_required
def treatment_delete(request, id):
    """Delete treatment method"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    treatment = get_object_or_404(TreatmentMethod, id=id)
    
    if request.method == 'POST':
        treatment_name = treatment.name
        treatment.delete()
        messages.success(request, f'Treatment "{treatment_name}" deleted!')
        return redirect('esg_treatment_list')
    
    return render(request, 'esg_tracking/treatment_confirm_delete.html', {'treatment': treatment})


# ========== ESG FACTOR CRUD ==========

@login_required
def esg_factor_list(request):
    """List all ESG factors"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    factors = ESGFactor.objects.select_related('sub_category__category', 'treatment').all()
    return render(request, 'esg_tracking/factor_list.html', {'factors': factors})


@login_required
def esg_factor_create(request):
    """Create new ESG factor"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    subcategories = WasteSubCategory.objects.filter(is_active=True)
    treatments = TreatmentMethod.objects.filter(is_active=True)
    
    if request.method == 'POST':
        subcategory_id = request.POST.get('sub_category')
        treatment_id = request.POST.get('treatment')
        co2_factor = request.POST.get('co2_factor')
        water_factor = request.POST.get('water_factor')
        trees_factor = request.POST.get('trees_factor')
        energy_factor = request.POST.get('energy_factor')
        source_standard = request.POST.get('source_standard')
        notes = request.POST.get('notes')
        
        subcategory = get_object_or_404(WasteSubCategory, id=subcategory_id)
        treatment = get_object_or_404(TreatmentMethod, id=treatment_id)
        
        if ESGFactor.objects.filter(sub_category=subcategory, treatment=treatment).exists():
            messages.error(request, f'Factor for {subcategory.name} → {treatment.name} already exists!')
        else:
            ESGFactor.objects.create(
                sub_category=subcategory,
                treatment=treatment,
                co2_factor=co2_factor,
                water_factor=water_factor,
                trees_factor=trees_factor,
                energy_factor=energy_factor,
                source_standard=source_standard,
                notes=notes,
                last_edited_by=request.user.username
            )
            messages.success(request, f'ESG Factor created for {subcategory.name} → {treatment.name}!')
            return redirect('esg_factor_list')
    
    return render(request, 'esg_tracking/factor_form.html', {
        'subcategories': subcategories,
        'treatments': treatments
    })


@login_required
def esg_factor_edit(request, id):
    """Edit ESG factor"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    factor = get_object_or_404(ESGFactor, id=id)
    subcategories = WasteSubCategory.objects.filter(is_active=True)
    treatments = TreatmentMethod.objects.filter(is_active=True)
    
    if request.method == 'POST':
        factor.sub_category_id = request.POST.get('sub_category')
        factor.treatment_id = request.POST.get('treatment')
        factor.co2_factor = request.POST.get('co2_factor')
        factor.water_factor = request.POST.get('water_factor')
        factor.trees_factor = request.POST.get('trees_factor')
        factor.energy_factor = request.POST.get('energy_factor')
        factor.source_standard = request.POST.get('source_standard')
        factor.notes = request.POST.get('notes')
        factor.last_edited_by = request.user.username
        factor.save()
        messages.success(request, f'ESG Factor updated!')
        return redirect('esg_factor_list')
    
    return render(request, 'esg_tracking/factor_form.html', {
        'factor': factor,
        'subcategories': subcategories,
        'treatments': treatments
    })


@login_required
def esg_factor_delete(request, id):
    """Delete ESG factor"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    factor = get_object_or_404(ESGFactor, id=id)
    
    if request.method == 'POST':
        factor_name = f"{factor.sub_category.name} → {factor.treatment.name}"
        factor.delete()
        messages.success(request, f'ESG Factor "{factor_name}" deleted!')
        return redirect('esg_factor_list')
    
    return render(request, 'esg_tracking/factor_confirm_delete.html', {'factor': factor})



from django.http import JsonResponse
from .models import WasteSubCategory, ESGFactor
from django.views.decorators.csrf import csrf_exempt

def get_sub_categories(request):
    """Return sub-categories for selected category"""
    category_id = request.GET.get('category_id')
    if category_id:
        subs = WasteSubCategory.objects.filter(category_id=category_id, is_active=True)
        data = [{'id': sub.id, 'name': sub.name} for sub in subs]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

def get_esg_factor(request):
    """Return ESG factor for selected sub-category and treatment"""
    sub_category_id = request.GET.get('sub_category')
    treatment_id = request.GET.get('treatment')
    
    if sub_category_id and treatment_id:
        factor = ESGFactor.objects.filter(
            sub_category_id=sub_category_id,
            treatment_id=treatment_id
        ).first()
        
        if factor:
            data = {
                'co2_factor': float(factor.co2_factor),
                'water_factor': float(factor.water_factor) if factor.water_factor else 0,
                'trees_factor': float(factor.trees_factor) if factor.trees_factor else 0,
            }
            return JsonResponse(data)
    
    return JsonResponse({'co2_factor': 0, 'water_factor': 0, 'trees_factor': 0})

def get_category_defaults(request):
    """Return default sub-category and treatment for a category"""
    category_id = request.GET.get('category_id')
    if category_id:
        category = WasteCategory.objects.filter(id=category_id).first()
        if category:
            data = {
                'default_sub_category': category.default_sub_category.id if category.default_sub_category else None,
                'default_treatment': category.default_treatment.id if category.default_treatment else None,
            }
            return JsonResponse(data)
    return JsonResponse({'default_sub_category': None, 'default_treatment': None})