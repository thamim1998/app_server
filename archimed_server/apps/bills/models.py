from django.db import models
from django.utils import timezone
from apps.investors.models import Investor
from datetime import date
from decimal import Decimal
from apps.investment.models import Investment
from apps.utils import get_current_year

class Bill(models.Model):
    BILL_TYPES = [
        ('membership', 'Membership'),
        ('upfront_fees', 'Upfront Fees'),
        ('yearly_fees', 'Yearly Fees'),
    ]

    investor = models.ForeignKey(Investor, related_name='bills', on_delete=models.CASCADE)   
    investment = models.ForeignKey(Investment, related_name='bills', on_delete=models.CASCADE)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    issue_date = models.DateTimeField(default=timezone.now)
    bill_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True) 
    capital = models.ForeignKey(
        'capital.Capital',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='related_bills'
    )       

    def __str__(self):
        return f'{self.bill_type} for {self.investor.name} - {self.amount}'
    
    @classmethod
    def create_membership_bills(cls, investor):
        current_year = get_current_year()
        subscriptions = []

        # Check if investor is eligible for subscription fees
        if investor.subscription_fee_waived:
            return {"error": "Investor has invested more than 50,000 EUR and is exempt from membership fees."}
        
        if not investor.is_active:
            return {"error": "Investor is not an active member."}
        
        if not investor.membership_year or investor.membership_year > current_year:
            return {"error": "Enter valid membership year"}

        # Generate bills for the years since the membership year up to the current year
        for year in range(investor.membership_year, current_year + 1):
            if cls.objects.filter(investor=investor, bill_type="membership", bill_year=year).exists():
                continue  # Skip if the bill already exists for the year

            # Subscription fee is a fixed amount
            subscription_fees = Decimal("3000.00")

            # Create a bill entry
            bill_data = {
                "investor": investor,
                "bill_type": "membership",
                "amount": subscription_fees,
                "bill_year": year,
                "description": f"Membership fee for year {year}"
            }

            bill = cls(**bill_data)
            bill.save()  # Save the bill in the database
            subscriptions.append(bill)

        if subscriptions:
            return subscriptions
        else:
            return {"message": "No new subscription bills created; all years already billed."}
    
    def calculate_upfront_fee(self):
        fee_percentage = self.investment.get_fee_percentage() / 100
        upfront_fee_amount = Decimal(fee_percentage * self.investment.investment_amount * 5).quantize(Decimal("0.01"))
        return upfront_fee_amount

    def calculate_yearly_fee(self,years_paid):
      fee_percentage = self.investment.fee_percentage() / 100  # 8.5% becomes 0.085

    # Case 1: Before April 2019
      if self.investor.invested_date < date(2019, 4, 1):
        print('Before April 2019')
        if years_paid == 1:
            # First-year fee based on partial year investment
            print('Amount',(Decimal((10.00) / 365) * fee_percentage * self.investor.invested_amount).quantize(Decimal("0.01")))
            yearly_fee = (Decimal((10.00) / 365) * fee_percentage * self.investor.invested_amount).quantize(Decimal("0.01"))
        else:
            # For subsequent years, use the fee percentage directly
            yearly_fee = (fee_percentage * self.investor.invested_amount).quantize(Decimal("0.01"))
      else:
        print('After April 2019')
        # Case 2: After April 2019
        if  years_paid == 1:
            # First-year fee calculation for investment after 2019, based on partial year
            print('First year after April 2019')
            yearly_fee = Decimal((10) * (fee_percentage) * self.investor.invested_amount).quantize(Decimal("0.01"))
        elif  years_paid == 2:
            # Second year: apply the original fee percentage
            print('Second year')
            yearly_fee = Decimal((fee_percentage) * self.investor.invested_amount).quantize(Decimal("0.01"))
        elif  years_paid == 3:
            # Third year: fee percentage reduced by 0.2%
            print('Third year')
            yearly_fee = Decimal((fee_percentage - Decimal(0.2 / 100)) * self.investor.invested_amount).quantize(Decimal("0.01"))
        elif  years_paid == 4:
            # Fourth year: fee percentage reduced by 0.5%
            print('Fourth year')
            yearly_fee = Decimal((fee_percentage - Decimal(0.5 / 100)) * self.investor.invested_amount).quantize(Decimal("0.01"))
        else:
            # For years after the fourth, reduce the fee by 1%
            print('Fifth year and beyond')
            yearly_fee = Decimal((fee_percentage - Decimal(1 / 100)) * self.investor.invested_amount).quantize(Decimal("0.01"))
      return yearly_fee
