from django.db import models

from authentication.models import Employee


# Create your models here.
class Timesheet(models.Model):
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    hours = models.FloatField(default=0)
    attachments = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="calendars")
