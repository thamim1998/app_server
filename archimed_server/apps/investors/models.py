from django.db import models
from django.utils import timezone

# Create your models here.

class Investor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    iban = models.CharField(max_length=34, unique=True) 
    invested_amount = models.DecimalField(max_digits=12, decimal_places=2) 
    fee_percentage = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    upfront_fees_paid = models.BooleanField(default=False)
    invested_date = models.DateField(default=timezone.now)
   
    @property
    def subscription_fee_waived(self):
        return self.invested_amount > 50000

    def __str__(self):
        return f"{self.name} ({self.email})"
