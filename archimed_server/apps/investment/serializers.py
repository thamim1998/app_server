from rest_framework import serializers
from .models import Investment

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields =['id','investor','investment_amount','investment_date','investment_type','fee_percentage','years_paid','bill_type_year']