from django.urls import path
from .views import get_all_bills,get_bill_by_investor,create_subscription,delete_bill,update_bill,create_upfront_fees,create_yearly_fees

urlpatterns = [
    path('bills/', get_all_bills, name = 'get_all_bills'),
    path('bills/create/membership/<int:investor_id>', create_subscription, name = 'create_subscription'),
    path('bills/create/upfrontfees/<int:investor_id>', create_upfront_fees, name = 'create_upfront_fees'),
    path('bills/create/yearlyfees/<int:investor_id>', create_yearly_fees, name = 'create_upfront_fees'),
    path('bills/update/<int:pk>', update_bill, name = 'update_bill'),
    path('bills/delete/<int:pk>', delete_bill, name='delete_bill'),
    path('bills/investor/<int:investor_id>',get_bill_by_investor, name='get_bill_by_investor')
]
