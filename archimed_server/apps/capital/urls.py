from django.urls import path
from .views import create_capital,get_all_capitals,delete_capital,update_capital

urlpatterns = [
    path('capital/', get_all_capitals, name = 'get_all_capitals'),
    path('capital/create', create_capital, name = 'create_capital'),
    path('capital/delete/<int:pk>', delete_capital, name = 'delete_capital'),
    path('capital/update/<int:pk>', update_capital, name = 'update_capital'),
]
