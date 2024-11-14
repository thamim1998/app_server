from rest_framework import serializers
from .models import Investor

class InvestorSerializer(serializers.ModelSerializer):
    subscription_fee_waived = serializers.ReadOnlyField()

    class Meta:
        model = Investor
        fields = ['id', 'name', 'email', 'iban', 'invested_amount', 'subscription_fee_waived', 'fee_percentage', 'invested_date']