# =============================================================================
# FILE    : schools/models.py
# APP     : schools
# PURPOSE : School profile, School-User assignment, Class, Section
# =============================================================================

import logging
from django.db import models
from accounts.models import User

logger = logging.getLogger(__name__)


# =============================================================================
# SCHOOL MODEL
# =============================================================================
class School(models.Model):

    class StatusChoices(models.TextChoices):
        ACTIVE   = 'active',   'Active'
        INACTIVE = 'inactive', 'Inactive'

    school_name      = models.CharField(max_length=255)
    short_name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    address          = models.TextField()
    city             = models.CharField(max_length=100)
    state            = models.CharField(max_length=100)
    latitude         = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude        = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    student_strength = models.PositiveIntegerField(default=0)
    status           = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.ACTIVE)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'schools'
        ordering = ['school_name']

    def __str__(self):
        return f"{self.school_name} - {self.city}"


# =============================================================================
# SCHOOL USER ASSIGNMENT
# =============================================================================
class SchoolUser(models.Model):

    class DesignationChoices(models.TextChoices):
        PRINCIPAL    = 'principal',    'Principal'
        TEACHER      = 'teacher',      'Teacher'
        PROJECT_HEAD = 'project_head', 'Project Head'

    school      = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school_users')
    user        = models.ForeignKey(User,   on_delete=models.CASCADE, related_name='school_assignments')
    designation = models.CharField(max_length=20, choices=DesignationChoices.choices)

    class Meta:
        db_table        = 'school_users'
        unique_together = ('school', 'user')

    def __str__(self):
        return f"{self.user.name} → {self.designation} at {self.school.school_name}"


# =============================================================================
# CLASS MODEL
# =============================================================================
class Class(models.Model):

    school     = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')
    class_name = models.CharField(max_length=50)

    class Meta:
        db_table        = 'classes'
        unique_together = ('school', 'class_name')
        ordering        = ['class_name']

    def __str__(self):
        return f"Class {self.class_name} - {self.school.school_name}"


# =============================================================================
# SECTION MODEL
# =============================================================================
class Section(models.Model):

    class_obj    = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='sections')
    section_name = models.CharField(max_length=10)

    class Meta:
        db_table        = 'sections'
        unique_together = ('class_obj', 'section_name')
        ordering        = ['section_name']

    def __str__(self):
        return f"Class {self.class_obj.class_name} - Section {self.section_name}"
    

class ReportingYear(models.Model):
    """
    Har school ka har saal ka reporting year track karega
    Jaise: Delhi Public School - 2024-2025
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('locked', 'Locked'),
    ]
    
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='reporting_years')
    year = models.CharField(max_length=9)  # "2024-2025"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'reporting_years'
        unique_together = ['school', 'year']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.school.school_name} - {self.year} ({self.status})"


# =============================================================================
# PRINCIPAL MODEL — Linked to School and User
# =============================================================================
class Principal(models.Model):
    """Principal profile linked to school"""
    
    class StatusChoices(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        PENDING = 'pending', 'Pending Approval'
    
    school = models.ForeignKey('School', on_delete=models.CASCADE, related_name='principals')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='principal_profile', null=True, blank=True)
    
    # Principal Details
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Account Status
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'principals'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.school.school_name}"
    
    def create_user_account(self, password='123'):
        """Create associated user account for login"""
        if not self.user:
            user = User.objects.create_user(
                username=self.email,
                password=password,
                name=self.name,
                email=self.email,
                phone=self.phone,
                role='principal',
                is_active=True,
                must_change_password=True
            )
            self.user = user
            self.save()
            return user
        return self.user