from rest_framework import serializers
from apps.bills.models import Bill
from .models import Capital

class CapitalSerializer(serializers.ModelSerializer):
    bills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Bill.objects.all()
    )
    class Meta:
        model = Capital
        fields = ['id', 'investor_id', 'bills', 'total_amount', 'status', 'issue_date','due_date']
