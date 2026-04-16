from django.db import models

# ============================================================
# 1. ICON MODEL — Sab Font Awesome icons yahan store honge
# ============================================================
class Icon(models.Model):
    """Font Awesome icons ka master table"""
    name = models.CharField(max_length=100, unique=True)  # e.g., "dashboard", "school"
    class_name = models.CharField(max_length=100)  # e.g., "fa-solid fa-gauge"
    category = models.CharField(max_length=50, blank=True)  # e.g., "navigation", "action"
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rbac_icons'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.class_name})"


# ============================================================
# 2. ROLE MODEL — Roles store honge
# ============================================================
class Role(models.Model):
    """User roles — Super Admin, Principal, Teacher, etc."""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rbac_roles'
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ============================================================
# 3. MENU MODEL — Parent aur child menu yahan store honge
# ============================================================
class Menu(models.Model):
    """Menu items — parent aur child dono"""
    name = models.CharField(max_length=100)
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, null=True, blank=True, related_name='menus')
    url = models.CharField(max_length=255, blank=True, null=True)  # "#" for parent menus
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rbac_menus'
        ordering = ['order', 'name']
    
    def __str__(self):
        if self.parent:
            return f"  └─ {self.name}"
        return self.name


# ============================================================
# 4. ROLE MENU PERMISSION — Role ko menu assign karna
# ============================================================
class RoleMenuPermission(models.Model):
    """Role ke liye menu permissions — view aur write"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='menu_permissions')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='role_permissions')
    can_view = models.BooleanField(default=False)   # Sidebar me dikhega?
    can_write = models.BooleanField(default=False)  # Add/Edit buttons dikhenge?
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rbac_role_menu_permissions'
        unique_together = ['role', 'menu']
    
    def __str__(self):
        return f"{self.role.name} → {self.menu.name} (V:{self.can_view}, W:{self.can_write})"