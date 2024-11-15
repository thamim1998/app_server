from django.urls import path
from .views import create_capital

urlpatterns = [
    path('capital/create', create_capital, name = 'create_capital'),
]
