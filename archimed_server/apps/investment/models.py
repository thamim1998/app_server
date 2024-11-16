from django.db import models
from apps.investors.models import Investor

class Investment(models.Model):
    
    investor = models.ForeignKey(Investor, related_name='investments', on_delete=models.CASCADE)
    investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_date = models.DateField()
    investment_type = models.CharField(max_length=50)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=3)
    years_paid = models.IntegerField(blank=True,default=1)
    upfront_fees_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Investment of {self.investment_amount} for {self.investor.name} ({self.investment_type})"
