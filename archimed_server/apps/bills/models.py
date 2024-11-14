from django.db import models
from django.utils import timezone
from apps.investors.models import Investor

class Bill(models.Model):
    BILL_TYPES = [
        ('membership', 'Membership'),
        ('upfront_fees', 'Upfront Fees'),
        ('yearly_fees', 'Yearly Fees'),
    ]

    investor = models.ForeignKey(Investor, related_name='bills', on_delete=models.CASCADE)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    issue_date = models.DateField(default=timezone.now().date)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.bill_type} for {self.investor.name} - {self.amount}'