from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class USer(AbstractUser):

    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

  
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
    )

    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.username
