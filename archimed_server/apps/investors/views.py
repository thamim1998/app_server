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

@api_view(['GET'])
def get_investor(request,pk):
    try:
        investors = Investor.objects.get(pk=pk)
        serializer = InvestorSerializer(investors).data   
        return Response(serializer, status=status.HTTP_202_ACCEPTED)
      
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    
@api_view(['GET'])
def handle_membership(request,pk):
    try:
        investor = Investor.objects.get(pk=pk)
        
        investor.is_active = not investor.is_active
        if(not investor.is_active):
            investor.membership_year = None
        investor.save()  

        return Response({"is_active": investor.is_active}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)