from django.db import models
from django.utils import timezone
from apps.investors.models import Investor
from datetime import date, datetime
from decimal import Decimal
from apps.investment.models import Investment
from apps.utils import get_current_date, get_current_year

class Bill(models.Model):
    BILL_TYPES = [
        ('membership', 'Membership'),
        ('upfront_fees', 'Upfront Fees'),
        ('yearly_fees', 'Yearly Fees'),
    ]

    investor = models.ForeignKey(Investor, related_name='bills', on_delete=models.CASCADE)   
    investment = models.ForeignKey(Investment,null=True, related_name='bills', on_delete=models.CASCADE)
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
    def create_bill(cls, investor, bill_type, amount, description, bill_year=None, investment=None, issue_date=None):
        """
        Class method to create a Bill instance with the given data.

        Args:
            investor (Investor): The associated investor.
            bill_type (str): The type of the bill (e.g., 'upfront_fees').
            amount (Decimal): The amount for the bill.
            description (str): A description of the bill.
            bill_year (int, optional): The year associated with the bill.
            investment (Investment, optional): The related investment, if any.
            issue_date (datetime, optional): The issue date of the bill.

        Returns:
            Bill: The created Bill object.
        """
        if not issue_date:
            issue_date = timezone.now()
        
        bill = cls.objects.create(
            investor=investor,
            investment=investment,
            bill_type=bill_type,
            amount=amount,
            description=description,
            bill_year=bill_year,
            issue_date=issue_date,
        )
        return bill
    
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

            bill = cls.create_bill(
            investor=investor,
            bill_type='membership',
            amount=subscription_fees,
            description=f"Membership fee for years {year}",
            bill_year=year
        )
            bill.save()
            subscriptions.append(bill)

        if subscriptions:
            return subscriptions
        else:
            return {"message": "No new subscription bills created; all years already billed."}
    
    @classmethod
    def calculate_next_upfront_year(cls, investment, increment):
        return investment.investment_date.year + investment.years_paid + increment
        
    
    @classmethod
    def generate_upfront_fee_bill(cls, investment, increment=5):
        """
        Generate and create an upfront fee bill for a specific investment.

        Args:
            investment (Investment): The investment for which the bill is generated.
            increment (int): Number of years for which upfront fees are paid (default is 5).

        Returns:
            Bill: The created Bill object.
        """
        # Ensure the investment is valid and calculate necessary values
        bill_year = cls.calculate_next_upfront_year(investment,increment)
        upfront_fee_amount = investment.calculate_upfront_fee()
        # Create the bill
        bill = cls.create_bill(
            investor=investment.investor,
            investment=investment,
            bill_type="upfront_fees",
            amount=upfront_fee_amount,
            description=f"Upfront fees paid till {bill_year}",
            bill_year=bill_year,
        )

        # Update investment's upfront fee status
        investment.upfront_fees_paid = True
        investment.years_paid += increment
        investment.save()

        return bill
    
    @classmethod
    def create_yearly_fees(cls, investment):
        current_year = get_current_year()
        current_date = get_current_date()
       
       # Get the associated investor
        investor = investment.investor

        # Check if upfront fees have already been paid for this year
        last_upfront_year = (
            max(investment.bill_type_year.get("upfront_fees", []))
            if "upfront_fees" in investment.bill_type_year else None
        )

        # Return error if upfront fees already cover the current year
        if last_upfront_year and last_upfront_year >= current_year:
            return {"error": "Investor has already paid upfront fees covering years beyond the current year."}

        yearly_fees = []
        years_paid = investment.years_paid  # Track the number of years fees have been paid
        
        for year in range(investment.investment_date.year, current_year + 1):  # +1 to include current year
            # Check if the yearly fee bill already exists for this year
            if cls.objects.filter(investor=investor, investment=investment, bill_type="yearly_fees", bill_year=year).exists():
                continue  # Skip if a bill already exists for this year

            # Create a new Bill instance for the current year
            bill = cls(investor=investor, investment=investment, bill_type="yearly_fees", issue_date=current_date)

            # Calculate the yearly fee using the calculate_yearly_fee method
            yearly_fee = bill.calculate_yearly_fee(years_paid)

            # Create a new bill and save it
            bill_data = cls.create_bill(
                investor=investor,
                investment=investment,
                bill_type="yearly_fees",
                amount=yearly_fee,
                description=f"Yearly subscription fee for {years_paid + 1}th year ({year} investment)",
                bill_year=year
            )

            # Increment the year of fee (1st, 2nd, etc.)
            years_paid += 1
            investment.years_paid = years_paid
            investment.save()

            yearly_fees.append(bill_data)

        return yearly_fees if yearly_fees else {"message": "No new yearly fee bills created; all years already billed."}

    def calculate_yearly_fee(self,years_paid):
      
      fee_percentage = self.investment.get_fee_percentage()  
      investment_date = self.investment.investment_date
      end_of_year = date(investment_date.year, 12, 31)
      remaining_days = (end_of_year - investment_date).days
      total_days_in_year = 366 if is_leap_year(self.investment.investment_date.year) else 365
      fraction_of_year = Decimal((end_of_year - investment_date).days) / Decimal(total_days_in_year)
      fee = fraction_of_year * fee_percentage * self.investment.investment_amount
      fee = fee.quantize(Decimal("0.01"))



    # Case 1: Before April 2019
      if self.investment.investment_date < date(2019, 4, 1):
        if years_paid == 0:
            # First-year fee based on partial year investment
            yearly_fee = fee

        else:
            # For subsequent years, use the fee percentage directly
            yearly_fee = (fee_percentage * self.investment.investment_amount).quantize(Decimal("0.01"))

      else:
        # Case 2: After April 2019
        if  years_paid == 0:
            # First-year fee calculation for investment after 2019, based on partial year
            yearly_fee = fee
 
        elif  years_paid == 1:
            # Second year: apply the original fee percentage
            yearly_fee = Decimal((fee_percentage) * self.investment.investment_amount).quantize(Decimal("0.01"))

        elif  years_paid == 2:
            # Third year: fee percentage reduced by 0.2%
            yearly_fee = Decimal((fee_percentage - Decimal(0.2 / 100)) * self.investment.investment_amount).quantize(Decimal("0.01"))

        elif  years_paid == 3:
            # Fourth year: fee percentage reduced by 0.5%
            yearly_fee = Decimal((fee_percentage - Decimal(0.5 / 100)) * self.investment.investment_amount).quantize(Decimal("0.01"))

        else:
            # For years after the fourth, reduce the fee by 1%
            yearly_fee = Decimal((fee_percentage - Decimal(1 / 100)) * self.investment.investment_amount).quantize(Decimal("0.01"))

      return yearly_fee

def is_leap_year(year):
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    return False