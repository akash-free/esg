from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recycler

# ========== VENDOR CRUD ==========

@login_required
def vendor_list(request):
    """All vendors list — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can view vendors.')
        return redirect('superadmin_dashboard')
    
    vendors = Recycler.objects.all().order_by('-created_at')
    return render(request, 'recycler_management/vendor_list.html', {'vendors': vendors})


@login_required
def vendor_create(request):
    """Add new vendor — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can add vendors.')
        return redirect('superadmin_dashboard')
    
    if request.method == 'POST':
        # Basic Info
        recycler_name = request.POST.get('recycler_name')
        vendor_type = request.POST.get('vendor_type')
        if vendor_type == 'other':
            new_type = request.POST.get('new_vendor_type', '').strip()
            if new_type:
                # Convert to lowercase and replace spaces with underscore
                vendor_type = new_type.lower().replace(' ', '_')
            else:
                messages.error(request, 'Please enter new vendor type name!')
                return render(request, 'recycler_management/vendor_form.html')
        
        status = request.POST.get('status', 'pending')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact_person = request.POST.get('contact_person')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        
        # Business Info
        gst_number = request.POST.get('gst_number')
        certifications = request.POST.get('certifications')
        
        # Operational Info
        processing_capacity = request.POST.get('processing_capacity', 0)
        recycling_efficiency = request.POST.get('recycling_efficiency', 0)
        minimum_quantity = request.POST.get('minimum_quantity', 0)
        pickup_schedule = request.POST.get('pickup_schedule')
        service_cities = request.POST.get('service_cities')
        
        # Performance Metrics
        trust_score = request.POST.get('trust_score', 0)
        
        # Notes
        notes = request.POST.get('notes')
        
        # Check if vendor already exists
        if Recycler.objects.filter(recycler_name=recycler_name).exists():
            messages.error(request, f'Vendor "{recycler_name}" already exists!')
            return render(request, 'recycler_management/vendor_form.html')
        
        # Create vendor
        vendor = Recycler.objects.create(
            recycler_name=recycler_name,
            vendor_type=vendor_type,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            contact_person=contact_person,
            contact_email=contact_email,
            contact_phone=contact_phone,
            gst_number=gst_number,
            certifications=certifications,
            processing_capacity=processing_capacity,
            recycling_efficiency=recycling_efficiency,
            minimum_quantity=minimum_quantity,
            pickup_schedule=pickup_schedule,
            service_cities=service_cities,
            trust_score=trust_score,
            status=status,
            notes=notes
        )
        
        messages.success(request, f'Vendor "{vendor.recycler_name}" created successfully!')
        return redirect('vendor_list')
    
    return render(request, 'recycler_management/vendor_form.html')


@login_required
def vendor_edit(request, id):
    """Edit vendor — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can edit vendors.')
        return redirect('superadmin_dashboard')
    
    vendor = get_object_or_404(Recycler, id=id)
    
    if request.method == 'POST':
        # Update all fields
        vendor.recycler_name = request.POST.get('recycler_name')
        vendor.vendor_type = request.POST.get('vendor_type')
        vendor_type = request.POST.get('vendor_type')
        if vendor_type == 'other':
            new_type = request.POST.get('new_vendor_type', '').strip()
            if new_type:
                vendor_type = new_type.lower().replace(' ', '_')
            else:
                messages.error(request, 'Please enter new vendor type name!')
                return render(request, 'recycler_management/vendor_form.html', {'vendor': vendor})
        vendor.vendor_type = vendor_type
        vendor.address = request.POST.get('address')
        vendor.city = request.POST.get('city')
        vendor.state = request.POST.get('state')
        vendor.pincode = request.POST.get('pincode')
        vendor.contact_person = request.POST.get('contact_person')
        vendor.contact_email = request.POST.get('contact_email')
        vendor.contact_phone = request.POST.get('contact_phone')
        vendor.gst_number = request.POST.get('gst_number')
        vendor.certifications = request.POST.get('certifications')
        vendor.processing_capacity = request.POST.get('processing_capacity', 0)
        vendor.recycling_efficiency = request.POST.get('recycling_efficiency', 0)
        vendor.minimum_quantity = request.POST.get('minimum_quantity', 0)
        vendor.pickup_schedule = request.POST.get('pickup_schedule')
        vendor.service_cities = request.POST.get('service_cities')
        vendor.trust_score = request.POST.get('trust_score', 0)
        vendor.status = request.POST.get('status', 'pending')
        vendor.notes = request.POST.get('notes')
        
        vendor.save()
        
        messages.success(request, f'Vendor "{vendor.recycler_name}" updated successfully!')
        return redirect('vendor_list')
    
    return render(request, 'recycler_management/vendor_form.html', {'vendor': vendor})


@login_required
def vendor_delete(request, id):
    """Delete vendor — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can delete vendors.')
        return redirect('superadmin_dashboard')
    
    vendor = get_object_or_404(Recycler, id=id)
    
    if request.method == 'POST':
        vendor_name = vendor.recycler_name
        vendor.delete()
        messages.success(request, f'Vendor "{vendor_name}" deleted successfully!')
        return redirect('vendor_list')
    
    return render(request, 'recycler_management/vendor_confirm_delete.html', {'vendor': vendor})