from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.bills.models import Bill
from apps.investors.models import Investor 
from .serializers import CapitalSerializer
from .models import Capital
from django.shortcuts import get_object_or_404

@api_view(["POST"])
def create_capital(request):
    investor_id = request.data.get("investor_id")
    bill_ids = request.data.get("bill_ids", [])
    due_date = request.data.get("due_date")

    if not len(bill_ids):
        return Response({"error": "Atleast one bill is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the investor_id is provided
    if not investor_id:
        return Response({"error": "Investor ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    bills = Bill.objects.filter(id__in=bill_ids, investor_id=investor_id)

    if bills.count() != len(bill_ids):
        return Response({"error": "One or more bills doesn't belong to this investor."}, status=status.HTTP_400_BAD_REQUEST)

    if bills.count() != len(bill_ids):
        return Response({"error": "One or more bills do not belong to this investor."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if any of the bills are already associated with a capital call
    duplicate_bills = bills.filter(capital_calls__isnull=False)
    if duplicate_bills.exists():
        return Response(
            {"error": "Invoice has already been generated for one or more of these bills."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Calculate the total amount
    total_amount = sum(bill.amount for bill in bills)

    # Prepare capital data
    capital_data = {
        "investor": investor_id,
        "total_amount": total_amount,
        "status": "pending",
        "due_date": due_date,
        "bills":[bill.id for bill in bills]
    }

    # Serialize and save the capital call
    serializer = CapitalSerializer(data=capital_data)
    investor = get_object_or_404(Investor, id=investor_id)

    if serializer.is_valid():
        capital = serializer.save(investor = investor)
        capital.bills.set(bills)
        for bill in bills:
            bill.capital = capital  # Assign the capital to the bill
            bill.save()  # Save each bi
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_capitals(request):
      try:
        capitals = Capital.objects.all()
        serializer = CapitalSerializer(capitals, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
      except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
@api_view(['GET'])
def get_capital(request,pk):
      try:
        capitals = Capital.objects.get(pk=pk)
        serializer = CapitalSerializer(capitals)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
      
      except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_investor_capitals(request,investor_id):
    try:
        capitals = Capital.objects.filter(investor_id=investor_id)
        if not capitals:
            return Response({"Detail":"No invoice found for this investor"},status=status.HTTP_204_NO_CONTENT)
        
        serializer = CapitalSerializer(capitals,many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    
    except Capital.DoesNotExist:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['DELETE'])
def delete_capital(request, pk):
    try:
        capital = Capital.objects.get(pk=pk)
        bills = Bill.objects.filter(id__in=capital.bills.values_list('id', flat=True))

    except Capital.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    for bill in bills:
        bill.capital = None
        bill.save()
    
    capital.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['PATCH'])
def update_capital(request, pk):
    try:
        capital = Capital.objects.get(pk=pk)

    except Capital.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CapitalSerializer(capital, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"Detail":"Successfully validated the billl"},status=status.HTTP_202_ACCEPTED)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

