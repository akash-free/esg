from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Role, Menu, Icon, RoleMenuPermission

# ========== ROLE MANAGEMENT ==========

@login_required
def role_list(request):
    """All roles dikhao"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    roles = Role.objects.all()
    return render(request, 'rbac/role_list.html', {'roles': roles})

@login_required
def role_create(request):
    """Naya role create karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Role.objects.filter(name=name).exists():
            messages.error(request, f'Role "{name}" already exists!')
        else:
            Role.objects.create(name=name, description=description)
            messages.success(request, f'Role "{name}" created successfully!')
            return redirect('role_list')
    
    return render(request, 'rbac/role_form.html')

@login_required
def role_edit(request, id):
    """Role edit karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    role = get_object_or_404(Role, id=id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if Role.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request, f'Role "{name}" already exists!')
        else:
            role.name = name
            role.description = description
            role.save()
            messages.success(request, f'Role "{name}" updated successfully!')
            return redirect('role_list')
    
    return render(request, 'rbac/role_form.html', {'role': role})

@login_required
def role_delete(request, id):
    """Role delete karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    role = get_object_or_404(Role, id=id)
    
    if request.method == 'POST':
        role_name = role.name
        role.delete()
        messages.success(request, f'Role "{role_name}" deleted successfully!')
        return redirect('role_list')
    
    return render(request, 'rbac/role_confirm_delete.html', {'role': role})


# ========== MENU MANAGEMENT ==========

@login_required
def menu_list(request):
    """All menus dikhao"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    menus = Menu.objects.all()
    return render(request, 'rbac/menu_list.html', {'menus': menus})

@login_required
def menu_create(request):
    """Naya menu create karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    icons = Icon.objects.all()
    parent_menus = Menu.objects.filter(parent__isnull=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        icon_id = request.POST.get('icon')
        url = request.POST.get('url')
        parent_id = request.POST.get('parent')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        icon = Icon.objects.get(id=icon_id) if icon_id else None
        parent = Menu.objects.get(id=parent_id) if parent_id else None
        
        Menu.objects.create(
            name=name,
            icon=icon,
            url=url,
            parent=parent,
            order=order,
            is_active=is_active
        )
        messages.success(request, f'Menu "{name}" created successfully!')
        return redirect('menu_list')
    
    return render(request, 'rbac/menu_form.html', {
        'icons': icons,
        'parent_menus': parent_menus
    })

@login_required
def menu_edit(request, id):
    """Menu edit karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    menu = get_object_or_404(Menu, id=id)
    icons = Icon.objects.all()
    parent_menus = Menu.objects.filter(parent__isnull=True).exclude(id=id)
    
    if request.method == 'POST':
        menu.name = request.POST.get('name')
        icon_id = request.POST.get('icon')
        menu.url = request.POST.get('url')
        parent_id = request.POST.get('parent')
        menu.order = request.POST.get('order', 0)
        menu.is_active = request.POST.get('is_active') == 'on'
        
        menu.icon = Icon.objects.get(id=icon_id) if icon_id else None
        menu.parent = Menu.objects.get(id=parent_id) if parent_id else None
        
        menu.save()
        messages.success(request, f'Menu "{menu.name}" updated successfully!')
        return redirect('menu_list')
    
    return render(request, 'rbac/menu_form.html', {
        'menu': menu,
        'icons': icons,
        'parent_menus': parent_menus
    })

@login_required
def menu_delete(request, id):
    """Menu delete karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    menu = get_object_or_404(Menu, id=id)
    
    if request.method == 'POST':
        menu_name = menu.name
        menu.delete()
        messages.success(request, f'Menu "{menu_name}" deleted successfully!')
        return redirect('menu_list')
    
    return render(request, 'rbac/menu_confirm_delete.html', {'menu': menu})


# ========== PERMISSION MANAGEMENT ==========

@login_required
def permission_list(request):
    """All permissions dikhao"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    permissions = RoleMenuPermission.objects.select_related('role', 'menu').all()
    return render(request, 'rbac/permission_list.html', {'permissions': permissions})

@login_required
def permission_create(request):
    """Naya permission assign karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    roles = Role.objects.all()
    menus = Menu.objects.all()
    
    if request.method == 'POST':
        role_id = request.POST.get('role')
        menu_id = request.POST.get('menu')
        can_view = request.POST.get('can_view') == 'on'
        can_write = request.POST.get('can_write') == 'on'
        
        role = Role.objects.get(id=role_id)
        menu = Menu.objects.get(id=menu_id)
        
        # Check if already exists
        perm, created = RoleMenuPermission.objects.get_or_create(
            role=role,
            menu=menu,
            defaults={'can_view': can_view, 'can_write': can_write}
        )
        
        if not created:
            perm.can_view = can_view
            perm.can_write = can_write
            perm.save()
            messages.success(request, f'Permission updated for {role.name} → {menu.name}')
        else:
            messages.success(request, f'Permission assigned for {role.name} → {menu.name}')
        
        return redirect('permission_list')
    
    return render(request, 'rbac/permission_form.html', {
        'roles': roles,
        'menus': menus
    })

@login_required
def permission_edit(request, id):
    """Permission edit karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    perm = get_object_or_404(RoleMenuPermission, id=id)
    
    if request.method == 'POST':
        perm.can_view = request.POST.get('can_view') == 'on'
        perm.can_write = request.POST.get('can_write') == 'on'
        perm.save()
        messages.success(request, f'Permission updated for {perm.role.name} → {perm.menu.name}')
        return redirect('permission_list')
    
    return render(request, 'rbac/permission_edit.html', {'perm': perm})

@login_required
def permission_delete(request, id):
    """Permission delete karo"""
    if request.user.role != 'superadmin':
        messages.error(request, 'Access denied')
        return redirect('superadmin_dashboard')
    
    perm = get_object_or_404(RoleMenuPermission, id=id)
    
    if request.method == 'POST':
        role_name = perm.role.name
        menu_name = perm.menu.name
        perm.delete()
        messages.success(request, f'Permission removed for {role_name} → {menu_name}')
        return redirect('permission_list')
    
    return render(request, 'rbac/permission_confirm_delete.html', {'perm': perm})