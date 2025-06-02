from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from permissions.permissions import HasPermission
from incomes.models import Income
from expenses.models import Expense
from django.db.models import Sum
from django.utils import timezone

# Create your views here.

class FinancialSummaryReportView(APIView):
    permission_classes = [IsAuthenticated, HasPermission('can_view_report')]
    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated(), HasPermission('can_view_report')]

    def get(self, request):
        user = request.user
        current_year = timezone.now().year

        # Group by month for the current year
        income_data = (
            Income.objects.filter(user=user, date__year=current_year, status=True, deleted_at__isnull=True)
            .values_list('date__month')
            .annotate(total_income=Sum('income_amount'))
            .order_by('date__month')
        )
        expense_data = (
            Expense.objects.filter(user=user, date__year=current_year, status=True, deleted_at__isnull=True)
            .values_list('date__month')
            .annotate(total_expense=Sum('spent_amount'))
            .order_by('date__month')
        )

        # Prepare month-wise summary
        summary = {}
        for month, total_income in income_data:
            summary.setdefault(month, {})['total_income'] = float(total_income or 0)
        for month, total_expense in expense_data:
            summary.setdefault(month, {})['total_expense'] = float(total_expense or 0)
        # Fill missing months
        for m in range(1, 13):
            summary.setdefault(m, {})
            summary[m].setdefault('total_income', 0.0)
            summary[m].setdefault('total_expense', 0.0)
            summary[m]['net_income'] = summary[m]['total_income'] - summary[m]['total_expense']

        # Convert to sorted list
        result = [
            {
                'month': m,
                'total_income': summary[m]['total_income'],
                'total_expense': summary[m]['total_expense'],
                'net_income': summary[m]['net_income'],
            }
            for m in range(1, 13)
        ]
        return Response({'year': current_year, 'monthly_summary': result})
