from django.urls import path
from .views import index, CommissionListView, CommissionDetailView, CommissionCreateView

urlpatterns = [
    path('', index, name='commissions'),
    path('list/', CommissionListView.as_view(), name='commission_list'),
    path('detail/<int:pk>', CommissionDetailView.as_view(), name='commission_detail'),
    path('add/', CommissionCreateView.as_view(), name="commission_add")
]

app_name = 'commissions'