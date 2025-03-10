from django.db import models
from django.contrib.auth.models import User

class Module(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_installed = models.BooleanField(default=False)
    version = models.CharField(max_length=10, default="1.0.0")
    latest_version = models.CharField(max_length=10, default="1.0.0")

    def __str__(self):
        return self.name
    
    @property
    def has_update(self):
        return self.latest_version > self.version


class Role(models.Model):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('user', 'User'),
        ('public', 'Public'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='public')