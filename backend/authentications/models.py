from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone



class User(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(max_length = 255, unique=True, verbose_name="email")
    firstName = models.CharField(max_length= 100, verbose_name="firstName")
    lastName = models.CharField(max_length= 100, verbose_name="lastName")
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    # is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # refresh_token = models.TextField(null=True, blank=True)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Nhân viên'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["firstName", "lastName"]
    def __str__(self):
        return self.email
    
    def full_name(self):
        return f"{self.firstName} {self.lastName}"
    
    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),       
            'access': str(refresh.access_token),
        }
    def save(self, *args, **kwargs):
        if self.role == "admin":
            self.is_superuser = True
            self.is_staff = True
        else: 
            self.is_superuser = False
            self.is_staff = False
        super().save(*args, **kwargs)


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)
    blacklisted_at = models.DateTimeField(default=timezone.now)


class oneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null = False, blank=True)
    def __str__(self):
        return f"OTP for {self.user.firstName}-passcode"