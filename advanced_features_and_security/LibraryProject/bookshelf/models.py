from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here. 
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The email field is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True) 
        return self.create_user(username, email, password, **extra_fields) 
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True) 

    #the deafukt object it will use is UserManager that onky accepts ussername andpassword
    #we have to tell it to use our cutom userMnager 
    objects = CustomUserManager() 
    REQUIRED_FIELDS = ['email', 'date_of_birth'] 
    USERNAME_FIELD = 'username' 

    def __str__(self):
         return f"{self.email} ({self.username})"  # ✅ this returns a string


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name  # ✅ Required by checker


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("can_create", "Can create"),
            ("can_view", "Can view book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return self.title  # ✅ Just return title


class Library(models.Model):
    title = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return self.title  # ✅ Only return title


class Librarian(models.Model):
    title = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.title  # ✅ Only return title


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"