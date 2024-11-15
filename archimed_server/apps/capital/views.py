from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.bills.models import Bill 
from .serializers import CapitalSerializer
from .models import Capital

@api_view(['POST'])
def create_capital(request):
    investor_id = request.data.get("investor_id")
    bill_ids = request.data.get("bill_ids",[])

    if not investor_id:
        return Response({"error":"Investor ID is required."},status=status.HTTP_400_BAD_REQUEST)
    
    if not bill_ids:
        return Response({"error: Atleast one bill id is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    bills = Bill.objects.filter(id__in=bill_ids, investor_id=investor_id)
    if bills.count() != len(bill_ids):
        return Response({"error":"One or more bills doesnt belong specific investors"}, status=status.HTTP_400_BAD_REQUEST)
    
    total_amount = sum(bill.amount for bill in bills)
    print(total_amount)
    return Response(status=status.HTTP_201_CREATED)

    # serializer = InvestorSerializer(data=request.data)
    
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)