from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index_view_url'),
    path('profile', user_profile, name='user_profile'),
    path('customer-info', CustomerCreate, name='customer_info_url'),
    path('installation_troublshooting', installation_view, name="ins_trob_url"),
    path('customer-contract', CustomerContract, name='customer-contract-url'),
    path('report', Report, name="report_url"),
    path('input-stock', InputStockView, name='input-stock-url'),
    path('record-goods', RecordView, name='record-url'),
    path('contract-report/<pk>', CustomerContractReport, name='customer_report_url'),
]
