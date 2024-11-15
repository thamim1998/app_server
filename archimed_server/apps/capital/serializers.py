from rest_framework import serializers
from .models import Capital

class CapitalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Capital
        fields = ['id', 'investor_id', 'bills', 'total_amount', 'status', 'issue_date','due_date']
