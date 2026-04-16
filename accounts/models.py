

import logging
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Debug logger
logger = logging.getLogger(__name__)


# =============================================================================
# ROLE CHOICES
# Yahan sab 5 roles define hain
# Aage jake role check karke dashboard redirect hoga
# =============================================================================
class RoleChoices(models.TextChoices):
    SUPER_ADMIN     = 'superadmin',     'Super Admin'
    PRINCIPAL       = 'principal',      'Principal'
    TEACHER         = 'teacher',        'Teacher'
    PROJECT_HEAD    = 'project_head',   'Project Head'
    RECYCLER_ADMIN  = 'recycler_admin', 'Recycler Admin'


# =============================================================================
# CUSTOM USER MANAGER
# create_user  → normal user banata hai
# create_superuser → terminal se superadmin banata hai
# =============================================================================

class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')

        user = self.model(username=username, **extra_fields)
        user.set_password(password)   # password hashed store hoga
        user.save(using=self._db)

        logger.debug(f"[UserManager] New user created → username: {username} | role: {extra_fields.get('role')}")
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        # Terminal se superadmin banane ke liye
        extra_fields.setdefault('role', RoleChoices.SUPER_ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', 'Super Admin')

        logger.debug(f"[UserManager] Superuser being created → username: {username}")
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # --- Login fields ---
    username    = models.CharField(max_length=150, unique=True)     # login ke liye
    password    = models.CharField(max_length=255)                  # auto hashed by Django
    must_change_password = models.BooleanField(default=False)

    # --- Profile fields ---
    name        = models.CharField(max_length=255)
    phone       = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    set_password_token = models.CharField(max_length=100, blank=True, null=True)
    token_created_at = models.DateTimeField(blank=True, null=True)
    school_id = models.IntegerField(null=True, blank=True)           # API se aaya school_id
    school_name = models.CharField(max_length=255, blank=True, null=True)  # API se aaya school name
    school_short_name = models.CharField(max_length=50, blank=True, null=True)  # API se aaya short name
    academic_year = models.CharField(max_length=20, blank=True, null=True)

    # --- Role (MOST IMPORTANT FIELD) ---
    # Yeh field decide karta hai user kaunsa dashboard dekhega
    role        = models.CharField(
                    max_length=20,
                    choices=RoleChoices.choices,
                    default=RoleChoices.TEACHER
                  )

    # --- Status ---
    is_active   = models.BooleanField(default=True)     # False = blocked user
    is_staff    = models.BooleanField(default=False)    # Django admin panel access

    # --- Timestamps ---
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    # Django ko batao login field kaunsa hai
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['name']   # createsuperuser command mein poochega

    objects = UserManager()

    class Meta:
        db_table    = 'users'           # PostgreSQL mein table ka naam
        ordering    = ['-created_at']

    def __str__(self):
        return f"{self.username} | {self.role} | {self.name}"

    # ---------------------------------------------------------
    # Role check helper properties
    # Views mein use karo: request.user.is_super_admin
    # ---------------------------------------------------------
    @property
    def is_super_admin(self):
        return self.role == RoleChoices.SUPER_ADMIN

    @property
    def is_principal(self):
        return self.role == RoleChoices.PRINCIPAL

    @property
    def is_teacher(self):
        return self.role == RoleChoices.TEACHER

    @property
    def is_project_head(self):
        return self.role == RoleChoices.PROJECT_HEAD

    @property
    def is_recycler_admin(self):
        return self.role == RoleChoices.RECYCLER_ADMIN