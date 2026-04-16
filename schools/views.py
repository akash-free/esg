from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ReportingYear
from .models import School, SchoolUser, Class, Section, ReportingYear, Principal
import traceback

@login_required
def school_list(request):
    """All schools list — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can view schools.')
        return redirect('superadmin_dashboard')
    
    schools = School.objects.all().order_by('-created_at')
    return render(request, 'schools/school_list.html', {'schools': schools})

@login_required
def school_create(request):
    """Add new school — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can add schools.')
        return redirect('superadmin_dashboard')
    
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        short_name = request.POST.get('short_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        student_strength = request.POST.get('student_strength', 0)
        status = request.POST.get('status', 'active')
        
        # Check if school already exists
        if School.objects.filter(school_name=school_name).exists():
            messages.error(request, f'School "{school_name}" already exists!')
        else:
            school = School.objects.create(
                school_name=school_name,
                short_name=short_name,
                address=address,
                city=city,
                state=state,
                student_strength=student_strength,
                status=status
            )
            messages.success(request, f'School "{school.school_name}" created successfully!')
            return redirect('school_list')
    
    return render(request, 'schools/school_form.html')

@login_required
def school_edit(request, id):
    """Edit school — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can edit schools.')
        return redirect('superadmin_dashboard')
    
    school = get_object_or_404(School, id=id)
    
    if request.method == 'POST':
        school.school_name = request.POST.get('school_name')
        school.short_name = request.POST.get('short_name')
        school.address = request.POST.get('address')
        school.city = request.POST.get('city')
        school.state = request.POST.get('state')
        school.student_strength = request.POST.get('student_strength', 0)
        school.status = request.POST.get('status', 'active')
        school.save()
        
        messages.success(request, f'School "{school.school_name}" updated successfully!')
        return redirect('school_list')
    
    return render(request, 'schools/school_form.html', {'school': school})

@login_required
def school_delete(request, id):
    """Delete school — Sirf Super Admin"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can delete schools.')
        return redirect('superadmin_dashboard')
    
    school = get_object_or_404(School, id=id)
    
    if request.method == 'POST':
        school_name = school.school_name
        school.delete()
        messages.success(request, f'School "{school_name}" deleted successfully!')
        return redirect('school_list')
    
    return render(request, 'schools/school_confirm_delete.html', {'school': school})


# ========== REPORTING YEAR CRUD ==========

@login_required
def reporting_year_list(request, school_id):
    """List all reporting years for a school"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can view reporting years.')
        return redirect('superadmin_dashboard')
    
    school = get_object_or_404(School, id=school_id)
    reporting_years = ReportingYear.objects.filter(school=school).order_by('-created_at')
    
    return render(request, 'schools/reporting_year_list.html', {
        'school': school,
        'reporting_years': reporting_years
    })


@login_required
def reporting_year_create(request, school_id):
    """Add new reporting year for a school"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can add reporting years.')
        return redirect('superadmin_dashboard')
    
    school = get_object_or_404(School, id=school_id)
    
    if request.method == 'POST':
        year = request.POST.get('year')
        status = request.POST.get('status', 'draft')
        
        # Check if year already exists for this school
        if ReportingYear.objects.filter(school=school, year=year).exists():
            messages.error(request, f'Reporting year {year} already exists for {school.school_name}!')
        else:
            ReportingYear.objects.create(
                school=school,
                year=year,
                status=status
            )
            messages.success(request, f'Reporting year {year} added for {school.school_name}!')
            return redirect('reporting_year_list', school_id=school.id)
    
    return render(request, 'schools/reporting_year_form.html', {'school': school})


@login_required
def reporting_year_edit(request, id):
    """Edit reporting year"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can edit reporting years.')
        return redirect('superadmin_dashboard')
    
    reporting_year = get_object_or_404(ReportingYear, id=id)
    school = reporting_year.school
    
    if request.method == 'POST':
        year = request.POST.get('year')
        status = request.POST.get('status')
        
        # Check if year already exists (excluding current)
        if ReportingYear.objects.filter(school=school, year=year).exclude(id=id).exists():
            messages.error(request, f'Reporting year {year} already exists for {school.school_name}!')
        else:
            reporting_year.year = year
            reporting_year.status = status
            reporting_year.save()
            messages.success(request, f'Reporting year updated successfully!')
            return redirect('reporting_year_list', school_id=school.id)
    
    return render(request, 'schools/reporting_year_form.html', {
        'school': school,
        'reporting_year': reporting_year
    })


@login_required
def reporting_year_delete(request, id):
    """Delete reporting year"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can delete reporting years.')
        return redirect('superadmin_dashboard')
    
    reporting_year = get_object_or_404(ReportingYear, id=id)
    school = reporting_year.school
    year_name = reporting_year.year
    
    if request.method == 'POST':
        reporting_year.delete()
        messages.success(request, f'Reporting year {year_name} deleted successfully!')
        return redirect('reporting_year_list', school_id=school.id)
    
    return render(request, 'schools/reporting_year_confirm_delete.html', {
        'school': school,
        'reporting_year': reporting_year
    })


@login_required
def reporting_year_activate(request, id):
    """Activate a reporting year (and deactivate others)"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can activate reporting years.')
        return redirect('superadmin_dashboard')
    
    reporting_year = get_object_or_404(ReportingYear, id=id)
    school = reporting_year.school
    
    # Deactivate all other reporting years for this school
    ReportingYear.objects.filter(school=school, status='active').update(status='draft')
    
    # Activate selected one
    reporting_year.status = 'active'
    reporting_year.save()
    
    messages.success(request, f'Reporting year {reporting_year.year} activated for {school.school_name}!')
    return redirect('reporting_year_list', school_id=school.id)


@login_required
def reporting_year_lock(request, id):
    """Lock a reporting year (after snapshot generation)"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can lock reporting years.')
        return redirect('superadmin_dashboard')
    
    reporting_year = get_object_or_404(ReportingYear, id=id)
    school = reporting_year.school
    
    reporting_year.status = 'locked'
    reporting_year.save()
    
    messages.success(request, f'Reporting year {reporting_year.year} locked for {school.school_name}!')
    return redirect('reporting_year_list', school_id=school.id)



from accounts.models import User
from .models import School, Principal
import random
import string

@login_required
def principal_list(request):
    """List all principals"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can view principals.')
        return redirect('superadmin_dashboard')
    
    principals = Principal.objects.select_related('school', 'user').all()
    return render(request, 'schools/principal_list.html', {'principals': principals})


# @login_required
# def principal_create(request):
#     """Add new principal"""
#     if request.user.role != 'superadmin':
#         messages.error(request, 'Access denied. Only Super Admin can add principals.')
#         return redirect('superadmin_dashboard')
    
#     schools = School.objects.filter(status='active')
    
#     if request.method == 'POST':
#         school_id = request.POST.get('school')
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
        
#         school = get_object_or_404(School, id=school_id)
        
#         # Check if principal with this email already exists
#         if Principal.objects.filter(email=email).exists():
#             messages.error(request, f'Principal with email {email} already exists!')
#         else:
#             # Create Principal
#             principal = Principal.objects.create(
#                 school=school,
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 status='active'
#             )
            
#             # Create associated user account with default password 123
#             user = principal.create_user_account(password='123')
            
#             messages.success(request, f'Principal "{name}" created successfully!')
#             messages.info(request, f'Login Details - Username: {email}, Password: 123 (Please change on first login)')
#             return redirect('principal_list')
    
#     return render(request, 'schools/principal_form.html', {'schools': schools})

# from .utils import send_principal_welcome_email

# @login_required
# def principal_create(request):
#     """Add new principal"""
#     if request.user.role != 'superadmin':
#         messages.error(request, 'Access denied. Only Super Admin can add principals.')
#         return redirect('superadmin_dashboard')
    
#     schools = School.objects.filter(status='active')
    
#     if request.method == 'POST':
#         school_id = request.POST.get('school')
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
        
#         school = get_object_or_404(School, id=school_id)
        
#         # Check if principal with this email already exists
#         if Principal.objects.filter(email=email).exists():
#             messages.error(request, f'Principal with email {email} already exists!')
#         else:
#             # Create Principal
#             principal = Principal.objects.create(
#                 school=school,
#                 name=name,
#                 email=email,
#                 phone=phone,
#                 status='active'
#             )
            
#             # Create associated user account with default password 123
#             user = principal.create_user_account(password='123')
            
#             # Send welcome email
#             try:
#                 email_sent = send_principal_welcome_email(
#                     principal_name=name,
#                     email=email,
#                     username=email,
#                     school_name=school.school_name
#                 )
#                 if email_sent:
#                     messages.success(request, f'Principal "{name}" created! Welcome email sent to {email}')
#                 else:
#                     messages.warning(request, f'Principal created but email could not be sent.')
#                     messages.info(request, f'Login Details - Username: {email}, Password: 123')
#             except Exception as e:
#                 messages.warning(request, f'Principal created. Login: {email} / Password: 123')
#                 print(f"Email error: {e}")
            
#             return redirect('principal_list')
    
#     return render(request, 'schools/principal_form.html', {'schools': schools})
from .utils import send_principal_set_password_email
import traceback  # ← ADD THIS IMPORT AT TOP

@login_required
def principal_create(request):
    """Add new principal"""
    print("=" * 50)
    print("STEP 1: principal_create function called")
    print("=" * 50)
    
    if request.user.role != 'superadmin':
        print("STEP 1.1: Access denied - not superadmin")
        messages.error(request, 'Access denied. Only Super Admin can add principals.')
        return redirect('superadmin_dashboard')
    
    schools = School.objects.filter(status='active')
    print(f"STEP 2: Schools loaded, count: {schools.count()}")
    
    if request.method == 'POST':
        print("STEP 3: POST request received")
        
        school_id = request.POST.get('school')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        print(f"STEP 4: Form data - School ID: {school_id}, Name: {name}, Email: {email}, Phone: {phone}")
        
        school = get_object_or_404(School, id=school_id)
        print(f"STEP 5: School found: {school.school_name}")
        
        # Check if principal with this email already exists
        if Principal.objects.filter(email=email).exists():
            print(f"STEP 6: Principal with email {email} already exists!")
            messages.error(request, f'Principal with email {email} already exists!')
        else:
            print("STEP 6: Principal email is unique, creating...")
            
            # Create Principal
            principal = Principal.objects.create(
                school=school,
                name=name,
                email=email,
                phone=phone,
                status='active'
            )
            print(f"STEP 7: Principal created with ID: {principal.id}")
            
            # ========== CREATE USER ==========
            print("STEP 8: Creating user account...")
            from accounts.models import User
            try:
                user = User.objects.create_user(
                    username=email,
                    password=None,  # ← No password
                    name=name,
                    email=email,
                    phone=phone,
                    role='principal',
                    is_active=False,  # ← Inactive until password set
                    must_change_password=False
                )
                print(f"STEP 9: User created with ID: {user.id}, Username: {user.username}")
                print(f"STEP 9.1: User is_active: {user.is_active}, must_change_password: {user.must_change_password}")
            except Exception as e:
                print(f"STEP 9 ERROR: User creation failed - {e}")
                traceback.print_exc()
                messages.error(request, f'User creation failed: {e}')
                return redirect('principal_list')
            
            principal.user = user
            principal.save()
            print(f"STEP 10: Principal linked to user: {principal.user.username}")
            
            # ========== SEND EMAIL ==========
            print("STEP 11: Attempting to send email...")
            try:
                from .utils import send_principal_set_password_email
                print("STEP 11.1: Import successful")
                
                email_sent = send_principal_set_password_email(
                    principal_name=name,
                    email=email,
                    username=email,
                    school_name=school.school_name,
                    user=user
                )
                print(f"STEP 12: Email sent result: {email_sent}")
                
                if email_sent:
                    messages.success(request, f'Principal "{name}" created! Set password email sent to {email}')
                    print("STEP 13: Success message - email sent")
                else:
                    messages.warning(request, f'Principal created but email could not be sent.')
                    print("STEP 13: Warning - email not sent")
                    
            except Exception as e:
                print(f"STEP 12 ERROR: Email sending failed - {e}")
                traceback.print_exc()
                messages.warning(request, f'Principal created. Email could not be sent.')
            
            return redirect('principal_list')
    
    print("STEP: Rendering form (GET request)")
    return render(request, 'schools/principal_form.html', {'schools': schools})


@login_required
def principal_edit(request, id):
    """Edit principal"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can edit principals.')
        return redirect('superadmin_dashboard')
    
    principal = get_object_or_404(Principal, id=id)
    schools = School.objects.filter(status='active')
    
    if request.method == 'POST':
        principal.school_id = request.POST.get('school')
        principal.name = request.POST.get('name')
        principal.email = request.POST.get('email')
        principal.phone = request.POST.get('phone')
        principal.status = request.POST.get('status', 'active')
        principal.save()
        
        # Update associated user account
        if principal.user:
            principal.user.name = principal.name
            principal.user.email = principal.email
            principal.user.phone = principal.phone
            principal.user.save()
        
        messages.success(request, f'Principal "{principal.name}" updated successfully!')
        return redirect('principal_list')
    
    return render(request, 'schools/principal_form.html', {
        'principal': principal,
        'schools': schools
    })


@login_required
def principal_delete(request, id):
    """Delete principal"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied. Only Super Admin can delete principals.')
        return redirect('superadmin_dashboard')
    
    principal = get_object_or_404(Principal, id=id)
    
    if request.method == 'POST':
        principal_name = principal.name
        
        # Delete associated user account
        if principal.user:
            principal.user.delete()
        
        principal.delete()
        messages.success(request, f'Principal "{principal_name}" deleted successfully!')
        return redirect('principal_list')
    
    return render(request, 'schools/principal_confirm_delete.html', {'principal': principal})


@login_required
def principal_reset_password(request, id):
    """Reset principal password to default '123'"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied.')
        return redirect('superadmin_dashboard')
    
    principal = get_object_or_404(Principal, id=id)
    
    if request.method == 'POST':
        if principal.user:
            principal.user.set_password('123')
            principal.user.must_change_password = True
            principal.user.save()
            messages.success(request, f'Password reset to "123" for {principal.name}')
        else:
            principal.create_user_account(password='123')
            messages.success(request, f'User account created with password "123" for {principal.name}')
        return redirect('principal_list')
    
    return render(request, 'schools/principal_reset_password.html', {'principal': principal})