from django.db import models
from apps.investors.models import Investor
from apps.bills.models import Bill

class Capital(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    investor = models.ForeignKey(Investor, on_delete=models.CASCADE, related_name="capital")
    bills = models.ManyToManyField(Bill, related_name="capital_calls")
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def __str__(self):
        return f"Capital Call for {self.investor.name} - {self.total_amount} EUR"
