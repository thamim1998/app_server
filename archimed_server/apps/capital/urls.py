from django.urls import path
from .views import create_capital,get_all_capitals,delete_capital,update_capital,get_investor_capitals,get_capital

urlpatterns = [
    path('capital/', get_all_capitals, name = 'get_all_capitals'),
    path('capital/<int:pk>', get_capital, name = 'get_capital'),
    path('capital/create', create_capital, name = 'create_capital'),
    path('capital/delete/<int:pk>', delete_capital, name = 'delete_capital'),
    path('capital/update/<int:pk>', update_capital, name = 'update_capital'),
    path('capital/investor/<int:investor_id>', get_investor_capitals, name = 'get_investor_capitals'),
]
