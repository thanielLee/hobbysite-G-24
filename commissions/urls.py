from django.urls import path
from .views import index, CommissionListView, CommissionDetailView

urlpatterns = [
    path('', index, name='commissions'),
    path('list', CommissionListView.as_view(), name='commission_list'),
    path('item/<int:pk>', CommissionDetailView.as_view(), name='commission_detail')
]

app_name = 'commissions'