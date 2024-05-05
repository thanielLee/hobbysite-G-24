from django.urls import path
from .views import index, CommissionListView, CommissionTemplateDetailView, CommissionCreateViewTemplate

urlpatterns = [
    path('', index, name='commissions'),
    path('list/', CommissionListView.as_view(), name='commission_list'),
    path('detail/<int:pk>', CommissionTemplateDetailView.as_view(), name='commission_detail'),
    path('add/', CommissionCreateViewTemplate.as_view(), name="commission_add")
]

app_name = 'commissions'