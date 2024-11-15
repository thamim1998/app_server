from django.db import models
from django.utils import timezone
from apps.investors.models import Investor
from datetime import date
from decimal import Decimal

class Bill(models.Model):
    BILL_TYPES = [
        ('membership', 'Membership'),
        ('upfront_fees', 'Upfront Fees'),
        ('yearly_fees', 'Yearly Fees'),
    ]

    investor = models.ForeignKey(Investor, related_name='bills', on_delete=models.CASCADE)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    bill_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)        

    def __str__(self):
        return f'{self.bill_type} for {self.investor.name} - {self.amount}'
    

    def calculate_yearly_fee(self, current_date,which_year):
    
      fee_percentage = self.investor.fee_percentage / 100  # 8.5% becomes 0.085

    # Case 1: Before April 2019
      if self.investor.invested_date < date(2019, 4, 1):
        print('Before April 2019')
        if which_year == 1:
            # First-year fee based on partial year investment
            yearly_fee = (Decimal(10.00) / 365) * self.investor.fee_percentage * self.investor.invested_amount
        else:
            # For subsequent years, use the fee percentage directly
            yearly_fee = self.investor.fee_percentage * self.investor.invested_amount
      else:
        print('After April 2019')
        # Case 2: After April 2019
        if  which_year == 1:
            # First-year fee calculation for investment after 2019, based on partial year
            print('First year after April 2019')
            yearly_fee = Decimal((10) * (fee_percentage) * self.investor.invested_amount).quantize(Decimal("0.01"))
        elif  which_year == 2:
            # Second year: apply the original fee percentage
            print('Second year')
            yearly_fee = Decimal((fee_percentage) * self.investor.invested_amount).quantize(Decimal("0.01"))
        elif  which_year == 3:
            # Third year: fee percentage reduced by 0.2%
            print('Third year')
            yearly_fee = Decimal((fee_percentage - Decimal(0.2 / 100)) * self.investor.invested_amount).quantize(Decimal("0.01"))
        elif  which_year == 4:
            # Fourth year: fee percentage reduced by 0.5%
            print('Fourth year')
            yearly_fee = Decimal((fee_percentage - Decimal(0.5 / 100)) * self.investor.invested_amount).quantize(Decimal("0.01"))
        else:
            # For years after the fourth, reduce the fee by 1%
            print('Fifth year and beyond')
            yearly_fee = Decimal((fee_percentage - Decimal(1 / 100)) * self.investor.invested_amount).quantize(Decimal("0.01"))
      return yearly_fee
