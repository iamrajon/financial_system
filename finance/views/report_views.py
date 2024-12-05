from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, F
from django.core.cache import cache
from finance.models import Income, Expense, Loan
from finance.serializers import ReportSerializer

class FinancialReportViewBase(GenericAPIView):
    """
    Base view for generating financial reports.
    """
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Define the base queryset for filtering purposes if needed.
        """
        user = self.request.user
        return {
            "income": Income.objects.filter(user=user),
            "expense": Expense.objects.filter(user=user),
            "loan": Loan.objects.filter(user=user, status=Loan.LoanStatus.ACTIVE),
        }

    def filter_by_date(self, queryset, start_date, end_date, date_field):
        """
        Filter the queryset by the given date range.
        """
        if start_date:
            queryset = queryset.filter(**{f"{date_field}__gte": start_date})
        if end_date:
            queryset = queryset.filter(**{f"{date_field}__lte": end_date})
        return queryset

    def aggregate_data(self, income_queryset, expense_queryset, loan_queryset):
        """
        Aggregate the financial data.
        """
        total_income = income_queryset.aggregate(total=Sum('amount'))['total'] or 0
        total_expenses = expense_queryset.aggregate(total=Sum('amount'))['total'] or 0
        active_loans = loan_queryset.aggregate(total_balance=Sum('remaining_balance'))['total_balance'] or 0
        return total_income, total_expenses, active_loans

    def get_trend_data(self, queryset, date_field):
        """
        Get trend data for visualization.
        """
        return (
            queryset.annotate(month=F(f'{date_field}__month'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

    def prepare_report_data(self, income_queryset, expense_queryset, loan_queryset):
        """
        Prepare the report data for response.
        """
        total_income, total_expenses, active_loans = self.aggregate_data(income_queryset, expense_queryset, loan_queryset)
        income_trend = self.get_trend_data(income_queryset, 'date_received')
        expense_trend = self.get_trend_data(expense_queryset, 'due_date')

        return {
            "summary": {
                "total_income": total_income,
                "total_expenses": total_expenses,
                "active_loans_balance": active_loans,
            },
            "visualization": {
                "income_trend": list(income_trend),
                "expense_trend": list(expense_trend),
            },
        }

class FinancialReportView(FinancialReportViewBase):
    """
    A view to generate financial reports dynamically using GenericAPIView.
    """

    def get(self, request, *args, **kwargs):
        # Parse and validate query parameters
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')

        # Retrieve querysets for filtering
        querysets = self.get_queryset()
        income_queryset = self.filter_by_date(querysets["income"], start_date, end_date, 'date_received')
        expense_queryset = self.filter_by_date(querysets["expense"], start_date, end_date, 'due_date')
        loan_queryset = querysets["loan"]

        # Prepare response data
        report_data = self.prepare_report_data(income_queryset, expense_queryset, loan_queryset)

        return Response(report_data)


class FinancialReportViewCached(FinancialReportViewBase):
    """
    A view to generate financial reports dynamically using GenericAPIView along with Caching.
    """

    def get(self, request, *args, **kwargs):
        # Parse and validate query parameters
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')

        # Generate a cache key
        cache_key = f"financial_report_{request.user.id}_{start_date or 'none'}_{end_date or 'none'}"
        cached_report = cache.get(cache_key)
        if cached_report:
            return Response(cached_report)

        # Retrieve querysets for filtering
        querysets = self.get_queryset()
        income_queryset = self.filter_by_date(querysets["income"], start_date, end_date, 'date_received')
        expense_queryset = self.filter_by_date(querysets["expense"], start_date, end_date, 'due_date')
        loan_queryset = querysets["loan"]

        # Prepare response data
        report_data = self.prepare_report_data(income_queryset, expense_queryset, loan_queryset)

        # Cache the report data
        cache.set(cache_key, report_data, timeout=3600)  # Cache for 1 hour

        return Response(report_data)

