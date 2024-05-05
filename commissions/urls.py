from django.urls import path
from .views import index, CommissionListView, CommissionTemplateDetailView, CommissionCreateViewTemplate, CommissionTemplateUpdateView

urlpatterns = [
    path('', index, name='commissions'),
    path('list/', CommissionListView.as_view(), name='commission_list'),
    path('detail/<int:pk>', CommissionTemplateDetailView.as_view(), name='commission_detail'),
    path('add/', CommissionCreateViewTemplate.as_view(), name="commission_add"),
    path('update/<int:commission_pk>', CommissionTemplateUpdateView.as_view(), name="commission_update")
]

app_name = 'commissions'