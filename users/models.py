from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Mở rộng User model với thông tin bổ sung"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USER_TYPE_CHOICES = [
        ('student', 'Học viên'),
        ('instructor', 'Giảng viên'),
        ('admin', 'Quản trị viên'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"