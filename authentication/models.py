from django.db import models
from django.contrib.auth.models import AbstractUser


class Employee(AbstractUser):
    manager = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="subordinates")
    is_admin = models.BooleanField(default=False)
