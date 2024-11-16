from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.investment.models import Investment
from apps.investment.serializers import InvestmentSerializer
from apps.investors.models import Investor
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def create_investment(request, investor_id):
    investor = get_object_or_404(Investor, id=investor_id)
    
    investment_data = {
        "investor": investor.id,
        "investment_amount": request.data.get('investment_amount'),
        "investment_date": request.data.get('investment_date'),
        "investment_type": request.data.get('investment_type'),
    }
    
    # Serialize and validate the data
    serializer = InvestmentSerializer(data=investment_data)
    if serializer.is_valid():
        serializer.save()  # Save the investment to the database
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_investments(request, investor_id):
    # Retrieve the investor
    investor = get_object_or_404(Investor, id=investor_id)
    
    # Get all investments of this investor
    investments = Investment.objects.filter(investor=investor)
    
    # Serialize and return investment data
    serializer = InvestmentSerializer(investments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
