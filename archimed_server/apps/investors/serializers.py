from rest_framework import serializers
from .models import Investor

class InvestorSerializer(serializers.ModelSerializer):
    subscription_fee_waived = serializers.ReadOnlyField()
    invested_amount = serializers.DecimalField(max_digits=15, decimal_places=2, default=0)


    class Meta:
        model = Investor
        fields = ['id', 'name', 'email', 'iban', 'invested_amount', 'subscription_fee_waived', 'membership_year','is_active']
