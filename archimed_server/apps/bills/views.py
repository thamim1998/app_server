from datetime import date, datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Bill
from .serializers import BillSerializer
from django.shortcuts import get_object_or_404
from apps.investors.models import Investor
from decimal import Decimal

@api_view(['GET'])
def get_all_bills(request):
      bills = Bill.objects.all()
      serializer = BillSerializer(bills, many=True)
      return Response(serializer.data)

@api_view(['POST'])
def create_bill(request):
     serializer = BillSerializer(data=request.data)
     if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_subscription(request, investor_id):
    subscriptions = []
    investor = get_object_or_404(Investor, id=investor_id)
    current_year = date.today().year

    if investor.subscription_fee_waived:
        return Response(
            {"error": "Investor has invested more than 50,000 EUR and is exempt from membership fees."},
            status=status.HTTP_400_BAD_REQUEST
        )

    for year in range(investor.invested_date.year, current_year + 1):
        if Bill.objects.filter(investor=investor, bill_type="membership", bill_year=year).exists():
            continue

        # Create the bill data
        subscription_fees = 3000
        bill_data = {
            "investor": investor.id,
            "bill_type": "membership",
            "amount": subscription_fees,
            "bill_year": year
        }
        print(f"Creating subscription for year {year}: {bill_data}")

        serializer = BillSerializer(data=bill_data)
        if serializer.is_valid():
            serializer.save() 
            subscriptions.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Return the list of created subscriptions
    if subscriptions:
        return Response(subscriptions, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"message": "No new subscription bills created; all years already billed."},
            status=status.HTTP_200_OK
        )
    
@api_view(['POST'])
def create_upfront_fees(request, investor_id):
    try:
        investor = get_object_or_404(Investor, id=investor_id)

        if investor.upfront_fees_paid:
            return Response(
                {"error": "Investor has already paid upfront fees and cannot be billed again for upfront fees."},
                status=status.HTTP_400_BAD_REQUEST
            )

        upfront_fee_amount = Decimal(investor.fee_percentage * investor.invested_amount * 5).quantize(Decimal("0.01"))
        print(upfront_fee_amount)

        bill_data = {
            "investor": investor.id,
            "bill_type": "upfront_fees",
            "amount": upfront_fee_amount,
            "description": request.data.get("description", "Upfront fees for investment"),
            "bill_year": date.today().year
        }

        serializer = BillSerializer(data=bill_data)
        if serializer.is_valid():
            serializer.save()

            investor.upfront_fees_paid = True
            investor.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_yearly_fees(request, investor_id):
    try:
        # Retrieve the investor
        investor = get_object_or_404(Investor, id=investor_id)

        # Ensure the investor hasn't already paid upfront fees
        if investor.upfront_fees_paid:
            return Response(
                {"error": "Investor has already paid upfront fees and cannot be billed for yearly fees."},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_date = date.today()  # Get the current date
        investment_date = investor.invested_date
        current_year = current_date.year

        yearly_fees = []
        which_year = 1  # Track the year in terms of fees (1st year, 2nd year, etc.)

        # Iterate through the years since the investment
        for year in range(investment_date.year, current_year + 1):  # +1 to include current year
            # Check if the yearly fee bill already exists for this year
            if Bill.objects.filter(investor=investor, bill_type="yearly_fees", bill_year=year).exists():
                # If a bill already exists for this year, skip it
                continue

            # Create a new Bill instance for the current year
            bill = Bill(investor=investor, bill_type="yearly_fees", issue_date=current_date)

            # Calculate the yearly fee using the calculate_yearly_fee method
            yearly_fee = bill.calculate_yearly_fee(current_date, which_year)

            # Prepare bill data
            bill_data = {
                "investor": investor.id,
                "bill_type": "yearly_fees",
                "amount": yearly_fee,
                "description": f"Yearly subscription fee for {which_year}th year ({year} investment)",
                "bill_year": year
            }
            print('current_year', year)

            # Serialize and save the bill
            serializer = BillSerializer(data=bill_data)
            if serializer.is_valid():
                # Save the bill instance
                # Increment the year of fee (1st, 2nd, etc.)
                which_year += 1
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