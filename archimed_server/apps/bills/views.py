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
def create_subscription(investor_id):
    investor = get_object_or_404(Investor, id=investor_id)
    if investor.invested_amount < 50000:
       subscription_fees = 3000
       bill_data = {
        "investor": investor.id,
        "bill_type": "membership",
        "amount": subscription_fees,
    }
    else:
        return Response(
            {"error": "Investor have invested more than 50,000 EUR"},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = BillSerializer(data=bill_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_upfront_fees(request,investor_id):

    investor = get_object_or_404(Investor, id=investor_id)
    
    fee_percentage = investor.fee_percentage / 100 
    upfront_fee_amount = round(fee_percentage * investor.invested_amount * 5, 2)

    bill_data = {
        "investor": investor.id,
        "bill_type": "upfront_fees",
        "amount": Decimal(upfront_fee_amount),
        "description": request.data.get("description", "Upfront fees for investment")
    }
    
    serializer = BillSerializer(data=bill_data)
    if serializer.is_valid():
        serializer.save()
        investor.upfront_fees_paid = True
        investor.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
def delete_bill(pk):
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
