from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.investment.models import Investment
from .models import Bill
from .serializers import BillSerializer
from django.shortcuts import get_object_or_404
from apps.investors.models import Investor
from apps.utils import get_current_year, get_current_date

@api_view(['GET'])
def get_all_bills(request):
      bills = Bill.objects.all()
      serializer = BillSerializer(bills, many=True)
      return Response(serializer.data)

@api_view(['POST'])
def create_subscription(request, investor_id):
    # Retrieve the investor object
    investor = get_object_or_404(Investor, id=investor_id)

    # Call the model's method to create the membership bills
    result = Bill.create_membership_bills(investor)

    # Handle the result returned by the model method
    if isinstance(result, list):  # If bills were created
        # Serialize the Bill objects and return them in the response
        serializer = BillSerializer(result, many=True)  # `many=True` to serialize a list of objects
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        # If there's an error or no bills were created
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def create_upfront_fees(request, investment_id):
    try:
        # Fetch the investment object
        investment = get_object_or_404(Investment, id=investment_id)
        investor = investment.investor  # Get the associated investor for this investment
        current_date = get_current_date()

        # Calculate the upfront fee using the helper method
        bill = Bill(investor=investor, investment=investment, bill_type="upfront_fees", issue_date=current_date)
        upfront_fee_amount = bill.calculate_upfront_fee()
        years_paid = investment.years_paid + 5
        investment_year = investment.investment_date.year + years_paid
        print(investment.investment_date.year, years_paid)

        bill_data = {
            "investor": investor.id,
            "investment": investment.id,
            "bill_type": "upfront_fees",
            "bill_year" : investment_year,
            "amount": upfront_fee_amount,
            "description": f"Upfront fees paid till {investment_year}"
        }
        # Serialize and save the bill
        serializer = BillSerializer(data=bill_data)
        if serializer.is_valid():
            serializer.save()

            # Update the investment's upfront fee status
            investment.upfront_fees_paid = True
            investment.years_paid = years_paid
            investment.bill_type_year["upfront_fees"].append(investment_year)
            investment.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def create_yearly_fees(request, investment_id):
    try:
        investment = get_object_or_404(Investment, id=investment_id)
        investor = investment.investor  # Get the associated investor for this investment
        investment_date = investment.investment_date
        current_year = get_current_year()
        current_date = get_current_date()

        last_upfront_year = (
            investment.bill_type_year["upfront_fees"][-1]
            if "upfront_fees" in investment.bill_type_year
            else None
        )

        print('lastFee',last_upfront_year)
        
        if last_upfront_year and last_upfront_year > current_year:
            return Response(
                {"error": "Investor has already paid upfront fees covering years beyond the current year."},
                status=status.HTTP_400_BAD_REQUEST
            )

        yearly_fees = []
        years_paid = investment.years_paid  # Track the year in terms of fees (1st year, 2nd year, etc.)
        print('years_paid', years_paid, investment_date.year)
        # Iterate through the years since the investment
        for year in range(investment_date.year, current_year + 1):  # +1 to include current year
            # Check if the yearly fee bill already exists for this year

            if Bill.objects.filter(investor=investor, investment=investment, bill_type="yearly_fees", bill_year=year).exists():
                # If a bill already exists for this year, skip it
                continue

            # Create a new Bill instance for the current year
            bill = Bill(investor=investor, investment=investment, bill_type="yearly_fees", issue_date=current_date)
            print('bill', bill)

            # Calculate the yearly fee using the calculate_yearly_fee method
            yearly_fee = bill.calculate_yearly_fee(years_paid)
            print('yearly_________paid')

            # Prepare bill data
            bill_data = {
                "investor": investor.id,
                "investment":investment_id,
                "bill_type": "yearly_fees",
                "amount": yearly_fee,
                "description": f"Yearly subscription fee for {years_paid+1}th year ({year} investment)",
                "bill_year": year
            }
            print('current_year', year)

            # Serialize and save the bill
            serializer = BillSerializer(data=bill_data)
            if serializer.is_valid():
                # Save the bill instance
                # Increment the year of fee (1st, 2nd, etc.)
                years_paid += 1
                investment.years_paid = years_paid
                investment.save()
                serializer.save()  # Save the bill after successful validation
                yearly_fees.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Return the list of created bills
        if yearly_fees:
            return Response(yearly_fees, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": "No new yearly fee bills created; all years already billed."},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_bill_by_investor(request,investor_id):
     try:
        bills = Bill.objects.filter(investor_id=investor_id)
        if not bills:
            return Response({"detail": "No bills found for this investor."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

     except Bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
     
@api_view(['DELETE'])
def delete_bill(request,pk):
    try:
        bill = Bill.objects.get(pk=pk)
    except Bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    bill.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def update_bill(request,pk):
    try:
        bill = Bill.objects.get(pk=pk)
    except Bill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BillSerializer(bill, data=request.data)
    if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
