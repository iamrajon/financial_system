from django.urls import path
from finance.views import income_views, expense_views, loan_views, report_views, logtest_views


urlpatterns = [
    # Income
    path('income/', income_views.IncomeListCreateView.as_view(), name='income-list-create'),
    # path('income/cached/', income_views.IncomeListCreateViewCached.as_view(), name='income-list-create-cached'),
    path('income/cached/', income_views.IncomeListCachedView.as_view(), name='income-list-cached'),
    path('income/<int:pk>/', income_views.IncomeRetrieveUpdateDeleteView.as_view(), name='income-detail'),

    # Expense
    path('expense/', expense_views.ExpenseListCreateView.as_view(), name="expense-list-create"),
    path('expense/cached/', expense_views.ExpenseListCachedView.as_view(), name="expense-list-cached"),
    path('expense/<int:pk>/', expense_views.ExpenseRetrieveUpdateDeleteView.as_view(),name="expense-detail"),

    # Loan
    path('loan/', loan_views.LoanListCreateView.as_view(), name="loan-list-create"),
    path('loan/cached/', loan_views.LoanListCachedView.as_view(), name="loan-list-cached"),
    path('loan/<int:pk>/', loan_views.LoanRetrieveUpdateDeleteView.as_view(), name="loan-detail"),

    # Report
    path('reports/', report_views.FinancialReportView.as_view(), name="financial-report"),
    path('reports/cached', report_views.FinancialReportView.as_view(), name="financial-report-cached"),

    # log test
    path('logtest/', logtest_views.my_view, name="logtest"),
]
