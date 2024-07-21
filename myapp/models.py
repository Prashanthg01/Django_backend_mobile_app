from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, UserID, password=None, **extra_fields):
        if not UserID:
            raise ValueError('The UserID field must be set')
        user = self.model(UserID=UserID, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, UserID, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(UserID, password, **extra_fields)

class MyUser(AbstractBaseUser):
    UserID = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = MyUserManager()

    USERNAME_FIELD = 'UserID'
    REQUIRED_FIELDS = ['email', 'name', 'phone_number']

    def __str__(self):
        return self.UserID

class UserCode(models.Model):
    user_id = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
class AttendanceData(models.Model):
    qr_code = models.CharField(max_length=100)
    user_ids = models.JSONField(default=list)  # List of user IDs
    created_at = models.DateTimeField(auto_now_add=True)