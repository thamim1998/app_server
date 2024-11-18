from django.forms import ValidationError
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
def create_upfront_fees(request,investment_id):
    try:
        # Fetch the investment and investor
        investment = get_object_or_404(Investment, id=investment_id)
        investor = investment.investor

        # Generate upfront fees via a model method
        bill = Bill.generate_upfront_fee_bill(investment)
        return Response(BillSerializer(bill).data, status=status.HTTP_201_CREATED)

    except ValidationError as e:
        return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "Unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['POST'])
# def create_yearly_fees(request, investment_id):
#     try:
#         investment = get_object_or_404(Investment, id=investment_id)
#         investor = investment.investor  # Get the associated investor for this investment
#         investment_date = investment.investment_date
#         current_year = get_current_year()
#         current_date = get_current_date()

#         last_upfront_year = (
#             max(investment.bill_type_year["upfront_fees"])
#             if "upfront_fees" in investment.bill_type_year
#             else None
#         )

        
#         if last_upfront_year and last_upfront_year >= current_year:
#             return Response(
#                 {"error": "Investor has already paid upfront fees covering years beyond the current year."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         yearly_fees = []
#         years_paid = investment.years_paid  # Track the year in terms of fees (1st year, 2nd year, etc.)
#         print('years_paid', years_paid, investment_date.year)
#         # Iterate through the years since the investment
#         for year in range(investment_date.year, current_year + 1):  # +1 to include current year
#             # Check if the yearly fee bill already exists for this year

#             if Bill.objects.filter(investor=investor, investment=investment, bill_type="yearly_fees", bill_year=year).exists():
#                 # If a bill already exists for this year, skip it
#                 continue

#             # Create a new Bill instance for the current year
#             bill = Bill(investor=investor, investment=investment, bill_type="yearly_fees", issue_date=current_date)
#             print('bill', bill)

#             # Calculate the yearly fee using the calculate_yearly_fee method
#             yearly_fee = bill.calculate_yearly_fee(years_paid)
#             print('yearly_________paid')

#             bill_data = Bill.create_bill(
#             investor=investor,
#             investment=investment,
#             bill_type="yearly_fee",
#             amount=yearly_fee,
#             description=f"Upfront fees paid till {year}",
#             bill_year=year
#         )

#             # Serialize and save the bill
#             serializer = BillSerializer(data=bill_data)
#             if serializer.is_valid():
#                 # Save the bill instance
#                 # Increment the year of fee (1st, 2nd, etc.)
#                 years_paid += 1
#                 investment.years_paid = years_paid
#                 investment.save()
#                 serializer.save()  # Save the bill after successful validation
#                 yearly_fees.append(serializer.data)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Return the list of created bills
#         if yearly_fees:
#             return Response(yearly_fees, status=status.HTTP_201_CREATED)
#         else:
#             return Response(
#                 {"message": "No new yearly fee bills created; all years already billed."},
#                 status=status.HTTP_200_OK
#             )

#     except Exception as e:
#         return Response(
#             {"error": str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR
#         )

@api_view(['POST'])
def create_yearly_fees(request, investment_id):
    try:
        # Fetch the investment and associated investor
        investment = get_object_or_404(Investment, id=investment_id)
        print(investment)

        # Call the model method to create the yearly fees bills
        yearly_fees_response = Bill.create_yearly_fees(investment)

        # Return the appropriate response based on the result
        if "error" in yearly_fees_response:
            return Response(yearly_fees_response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = BillSerializer(yearly_fees_response, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_bill_by_investor(request,investor_id):
     try:
        bill_type = request.query_params.get('bill_type', None)

        if bill_type:
            bills = Bill.objects.filter(investor_id=investor_id, bill_type=bill_type)
        else:
            bills = Bill.objects.filter(investor_id=investor_id)

        # Check if any bills are found
        if not bills.exists():
            return Response({"detail": "No bills found for the specified criteria."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the bills
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

     except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
     
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
