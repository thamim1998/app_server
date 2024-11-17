from django.urls import path
from apps.investment.views import get_all_investment,create_investment,get_investments,delete_investment

urlpatterns = [
    path('investment/create/<int:investor_id>', create_investment, name='create_investment'),
    path('investments/<int:investor_id>/', get_investments, name='get_investments'),
    path('investments/', get_all_investment, name = 'get_all_investment'),
    path('investment/delete/<int:investment_id>', delete_investment, name = 'get_all_investment'),

]
