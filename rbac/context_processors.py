from .models import RoleMenuPermission

def user_menu(request):
    """Har request me user ke role ke hisaab se menu fetch karega"""
    menu_data = []
    
    if request.user.is_authenticated:
        # User ke role ke liye permissions fetch karo
        permissions = RoleMenuPermission.objects.filter(
            role__name=request.user.role,
            can_view=True,
            menu__is_active=True
        ).select_related('menu', 'menu__icon')
        
        # Sab menus fetch karo
        all_menus = []
        for perm in permissions:
            menu = perm.menu
            all_menus.append({
                'id': menu.id,
                'name': menu.name,
                'icon': menu.icon.class_name if menu.icon else 'fa-solid fa-circle',
                'url': menu.url,
                'parent_id': menu.parent.id if menu.parent else None,
                'order': menu.order,
                'can_write': perm.can_write,
            })
        
        # Parent-Child hierarchy banao
        menu_dict = {}
        for menu in all_menus:
            menu_dict[menu['id']] = menu
            menu_dict[menu['id']]['children'] = []
        
        for menu in all_menus:
            if menu['parent_id']:
                parent = menu_dict.get(menu['parent_id'])
                if parent:
                    parent['children'].append(menu)
        
        # Parent menus fetch karo
        menu_data = [menu for menu in menu_dict.values() if not menu['parent_id']]
        # Sort by order
        menu_data.sort(key=lambda x: x['order'])
        for menu in menu_data:
            if menu['children']:
                menu['children'].sort(key=lambda x: x['order'])
        
    
    return {
        'user_menu': menu_data,
    }