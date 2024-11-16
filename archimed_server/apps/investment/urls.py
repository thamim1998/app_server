from django.urls import path
from apps.investment import views

urlpatterns = [
    path('create/<int:investor_id>/', views.create_investment, name='create_investment'),
    path('list/<int:investor_id>/', views.get_investments, name='get_investments'),
]
