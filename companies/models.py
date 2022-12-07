from django.db import models
from django.utils.timezone import now
from django.db.models import URLField


# Create your models here.
class Company(models.Model):
    class CompanyStatus(models.Choices):
        LAYOFFS = "Layoffs"
        HIRING_FREEZE = "Hiring freeze"
        HIRING = "Hiring"

    name = models.CharField(max_length=30, unique=True)
    status = models.CharField(
        max_length=14, choices=CompanyStatus.choices, default=CompanyStatus.HIRING
    )
    last_update = models.DateTimeField(default=now, editable=True)
    application_link = URLField(blank=True)
    notes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name
