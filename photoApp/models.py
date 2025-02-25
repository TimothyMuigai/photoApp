from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.utils.timezone import now

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(max_length=25,unique=True ,null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True)    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name    

class Photo(models.Model):
    title = models.CharField(max_length=25)
    description = models.TextField(max_length=200, null=False, blank=False)
    image = CloudinaryField("image",null = False)
    tags = models.ManyToManyField("Tag",blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_photo",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title

class Profile(models.Model):  
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    image = CloudinaryField("image", default='default_cl3qsg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'