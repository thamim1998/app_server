from rest_framework import serializers
from .models import Bill

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'investor', 'bill_type', 'amount','bill_year','capital', 'issue_date', 'description']

    
    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount should be positive.")
        return data
