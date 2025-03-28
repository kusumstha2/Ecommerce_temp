from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.core.validators import MinLengthValidator, RegexValidator
from .validators import phone_validator

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)  # Ensure user is active
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    gender = models.CharField(
        max_length=100,
        choices=[("male", "Male"), ("female", "Female"), ("others", "Others")],
        default="male"
    )
    password = models.CharField(max_length=300, validators=[MinLengthValidator(8)])
    username = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(
        max_length=10,
        validators=[phone_validator],
        help_text="Enter a 10-digit contact number",
        
    )
    

    role = models.ForeignKey(Group, related_name='user_groups', on_delete=models.CASCADE, default=3)
    is_active = models.BooleanField(default=True)
  
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True
    )

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)
        try:
            default_group = Group.objects.get(id=2)
        except Group.DoesNotExist:
            default_group = (
                None  # Or handle it differently, e.g., create the group if necessary
            )
        if default_group and not self.groups.exists():
            self.groups.add(default_group)

    def __str__(self):
        return self.email

  


