from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('seller', 'Seller'),
        ('bidder', 'Bidder'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # Store hashed passwords
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Required fields for custom user models
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Field to log in
    REQUIRED_FIELDS = ['name', 'role']  # Required fields other than USERNAME_FIELD

    def __str__(self):
        return f"{self.name} ({self.role})"

    @property
    def is_anonymous(self):
        return False  # Always return False for user objects

    @property
    def is_authenticated(self):
        return True  # Always return True for user objects
