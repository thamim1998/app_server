from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status 
from .serializers import InvestorSerializer
from .models import Investor

@api_view(['GET'])
def get_investors(request):
    investors = Investor.objects.all()
    serializedData = InvestorSerializer(investors, many=True).data
    return Response(serializedData)

@api_view(['POST'])
def create_investor(request):
    serializer = InvestorSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', 'PATCH'])
def handle_investor(request, pk):
    try:
        investor = Investor.objects.get(pk=pk)
    except Investor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':
        investor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PATCH':
        data = request.data
        serializer = InvestorSerializer(investor,data=data, partial=True)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    


