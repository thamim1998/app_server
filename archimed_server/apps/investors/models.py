from django.db import models
from django.utils import timezone

# Create your models here.

class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    iban = models.CharField(max_length=34, unique=True) 
    invested_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    membership_year = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.email})"
   
    @property
    def subscription_fee_waived(self):
        return self.invested_amount > 50000
