# tests/test_report_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from finance.models import Income, Expense, Loan
from accounts.models import User
from datetime import date

class FinancialReportViewsTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email="test.user@example.com", username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(email="test.user@example.com", password='testpass')

        # Create some test data
        self.income1 = Income.objects.create(
            user=self.user, 
            source_name='Job', 
            amount=1000, 
            date_received='2024-01-01', 
            status=Income.IncomeStatus.RECEIVED
        )
        self.income2 = Income.objects.create(
            user=self.user, 
            source_name='Freelance', 
            amount=500, 
            date_received='2024-10-01', 
            status=Income.IncomeStatus.PENDING
        )
        
        self.expense1 = Expense.objects.create(
            user=self.user, 
            category='Food', 
            amount=100, 
            due_date='2025-01-01', 
            status=Expense.ExpenseStatus.PAID
        )
        self.expense2 = Expense.objects.create(
            user=self.user, 
            category='Transport', 
            amount=50, 
            due_date='2025-02-01', 
            status=Expense.ExpenseStatus.PENDING
        )
        
        self.loan1 = Loan.objects.create(
            user=self.user, 
            loan_name='Car Loan', 
            principal_amount=5000, 
            interest_rate=5.0, 
            tenure_months=24, 
            remaining_balance=3000, 
            status=Loan.LoanStatus.ACTIVE
        )

    def test_financial_report_view(self):
        url = reverse('financial-report')  
        response = self.client.get(url, {'start_date': '2023-02-01', 'end_date': '2024-12-31'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('summary', response.data)
        self.assertIn('visualization', response.data)
        self.assertEqual(response.data['summary']['total_income'], 1500)
        self.assertEqual(response.data['summary']['total_expenses'], 0)
        self.assertEqual(response.data['summary']['active_loans_balance'], 3000)

   