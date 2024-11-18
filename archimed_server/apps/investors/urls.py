from django.urls import path
from .views import get_investors,create_investor, handle_investor,get_investor, handle_membership

urlpatterns = [
    path('investors/', get_investors, name = 'get_investors'),
    path('investors/create', create_investor, name = 'create_investor'),
    path('investors/<int:pk>', handle_investor, name = 'handle_investor'),
    path('investor/<int:pk>', get_investor, name = 'get_investor'),
    path('investor/membership/<int:pk>', handle_membership, name = 'handle_membership'),
]
