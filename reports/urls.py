from django.urls import path
from .views import FinancialSummaryReportView

urlpatterns = [
    path('financial-summary/', FinancialSummaryReportView.as_view(), name='financial-summary-report'),
] 