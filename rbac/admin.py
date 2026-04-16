from django.contrib import admin
from .models import Icon, Role, Menu, RoleMenuPermission

@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ['name', 'class_name', 'category', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'class_name']
    list_editable = ['is_active']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['is_active']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'url', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['name']
    list_editable = ['order', 'is_active']


@admin.register(RoleMenuPermission)
class RoleMenuPermissionAdmin(admin.ModelAdmin):
    list_display = ['role', 'menu', 'can_view', 'can_write']
    list_filter = ['role', 'can_view', 'can_write']
    search_fields = ['role__name', 'menu__name']
    list_editable = ['can_view', 'can_write']