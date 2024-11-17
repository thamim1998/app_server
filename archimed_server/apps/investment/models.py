from django.db import models
from apps.investors.models import Investor

class Investment(models.Model):
    
    investor = models.ForeignKey(Investor, related_name='investments', on_delete=models.CASCADE)
    investment_amount = models.DecimalField(max_digits=15, decimal_places=2)
    investment_date = models.DateField()
    investment_type = models.CharField(max_length=50)
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=3)
    years_paid = models.IntegerField(blank=True,default=0)
    upfront_fees_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Investment of {self.investment_amount} for {self.investor.name} ({self.investment_type})"
    
    @property
    def bill_type_year(self):
        from apps.bills.models import Bill
        bill_years = {}
        bills = Bill.objects.filter(investment=self).filter(bill_type__in=['yearly_fees', 'upfront_fees'])
        for bill in bills:
            print(bill)
            if bill.bill_type not in bill_years:
                bill_years[bill.bill_type] = []

            bill_years[bill.bill_type].append(bill.bill_year)

        return bill_years
    
    def get_fee_percentage(self):
        return self.fee_percentage / 100
