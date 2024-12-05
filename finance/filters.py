from django_filters import FilterSet, DateFilter, CharFilter, DateFromToRangeFilter, ChoiceFilter, NumberFilter
from finance.models import Income, Expense, Loan
from rest_framework.filters import BaseFilterBackend

# Dynamically filter Income of authenticated user with different fields
class IncomeFilter(FilterSet):
    # Define custom filters
    date_received = DateFilter(field_name='date_received', lookup_expr='exact')
    date_received_gt = DateFilter(field_name='date_received', lookup_expr='gt')
    date_received_range = DateFromToRangeFilter(field_name='date_received')
    # Use iexact for case-insensitive exact match
    source_name = CharFilter(field_name='source_name', lookup_expr='iexact')

    class Meta:
        model = Income
        fields = {
            'status': ['exact'],
            # 'source_name': ['exact', 'iexact']
            # 'source_name' is handled by custom filter above
        }

# Dynamically filter the Expense of authenticated user with different fields
class ExpenseFilter(FilterSet):
    due_date = DateFilter(field_name='due_date', lookup_expr='exact')
    due_date_gt = DateFilter(field_name='due_date', lookup_expr='gt')
    due_date_range = DateFromToRangeFilter(field_name='due_date')

    class Meta:
        model = Expense
        fields = {
            'category': ['iexact', 'exact'],
            'status': ['exact'],
            # 'due_date': ['exact', 'gt']
        }

# Dynamically filter the Loan of authenticated use with different fields
class LoanFilter(FilterSet):
    loan_name = CharFilter(
        field_name='loan_name', 
        lookup_expr='icontains', 
        help_text="Filter loans by name (case-insensitive)."
    )

    status = ChoiceFilter(
        field_name='status', 
        choices=Loan.LoanStatus.choices, 
        help_text="Filter loans by status (Active or Paid)."
    )

    remaining_balance_gte = NumberFilter(
        field_name='remaining_balance', 
        lookup_expr='gte', 
        help_text="Filter loans with remaining balance greater than or equal to the given value."
    )
    remaining_balance_lte = NumberFilter(
        field_name='remaining_balance', 
        lookup_expr='lte', 
        help_text="Filter loans with remaining balance less than or equal to the given value."
    )

    class Meta:
        model = Loan
        fields = ['loan_name', 'status', 'remaining_balance_gte', 'remaining_balance_lte']


# Creating Custom Dynamic FilterBackend
class CustomDynamicFilterBackend(BaseFilterBackend):
    """
    Custom filter backend to handle dynamic filtering and sorting.
    Supports query parameters like ?filter_field=value&sort_by=field&order=asc/desc.

    ** Example url for testing CustomDynamicFilterBackend:
    http://127.0.0.1:8000/finance/loan/?filter_status=paid&sort_by=remaining_balance&order=asc

    """
    def filter_queryset(self, request, queryset, view):
        # Handle dynamic filtering
        for param, value in request.query_params.items():
            if param.startswith('filter_'):
                field_name = param.replace('filter_', '')  # Extract the field name
                filter_condition = {field_name: value}
                queryset = queryset.filter(**filter_condition)

        # Handle sorting
        sort_by = request.query_params.get('sort_by')
        order = request.query_params.get('order', 'asc')  # Default to ascending
        if sort_by:
            if order == 'desc':
                sort_by = f"-{sort_by}"  # Add descending prefix
            queryset = queryset.order_by(sort_by)

        return queryset