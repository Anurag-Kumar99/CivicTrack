from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'user'),
        ('EMPLOYEE', 'employee'),
        ('ADMIN', 'admin'),
    )
    role = models.CharField(max_length=10, choices =ROLE_CHOICES, default='USER')
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


class Department(models.Model):
    name = models.CharField(max_length=100)
    # problem_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.department.name}"


class Complaint(models.Model):
    CATEGORY_CHOICES =[
        ('ROAD', 'road'),
        ('WATER', 'water'),
        ('ELECTRICITY', 'electricity'),
        ('SANITATION', 'sanitation'),
        ('GARBAGE', 'garbage'),
        ('general', 'general'),
    ]

    PRIORITY_CHOICES =[
        ('LOW', 'low'),
        ('MEDIUM', 'medium'),
        ('HIGH', 'high'),
    ]


    STATUS_CHOICES =(
        ('PENDING', 'pending'),
        ('ACCEPTED', 'accepted'),
        ('IN_PROGRESS', 'in_progress'),
        ('RESOLVED', 'resolved'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    assigned_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    user_image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    resolved_image = models.ImageField(upload_to='resolved_images/', blank=True, null=True)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general') 
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"



class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    ) 
    full_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)

    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

