from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.investment.models import Investment
from apps.investment.serializers import InvestmentSerializer
from apps.investors.models import Investor
from django.shortcuts import get_object_or_404
from decimal import Decimal


@api_view(['POST'])
def create_investment(request, investor_id):
    investor = get_object_or_404(Investor, id=investor_id)
    
    investment_data = request.data
    fee_percentage = investment_data.get('fee_percentage', None)

    investment_amount = Decimal(investment_data['investment_amount'])

    investment = Investment.objects.create(
        investment_amount=investment_amount,
        fee_percentage=fee_percentage,
        investment_type=investment_data['investment_type'],
        investment_date=investment_data['investment_date'],
        investor_id=investor_id
    )

    print('investor', investor)

    investor.invested_amount += investment_amount
    investor.save()

    serializer = InvestmentSerializer(investment)
    return Response(serializer.data)


@api_view(['GET'])
def get_investments(request, investor_id):
    investor = get_object_or_404(Investor, id=investor_id)
    
    investments = Investment.objects.filter(investor=investor)
    
    serializer = InvestmentSerializer(investments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_investment(request):
      bills = Investment.objects.all()
      serializer = InvestmentSerializer(bills, many=True)
      return Response(serializer.data)