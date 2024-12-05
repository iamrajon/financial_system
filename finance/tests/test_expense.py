# tests/test_expense_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from finance.models import Expense
from accounts.models import User

class ExpenseViewsTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email="test.user@example.com", username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(email="test.user@example.com", password='testpass')

        # Create some test expense data
        self.expense1 = Expense.objects.create(user=self.user, category='Food', amount=100, due_date='2025-01-01', status=Expense.ExpenseStatus.PAID)
        self.expense2 = Expense.objects.create(user=self.user, category='Transport', amount=50, due_date='2025-02-01', status=Expense.ExpenseStatus.PAID)

    def test_expense_list_create_view(self):
        # Test GET request
        url = reverse('expense-list-create')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['category'], 'Food')

        # Test POST request
        data = {'category': 'Entertainment', 'amount': 200.00, 'due_date': '2025-03-01', 'status': f'{Expense.ExpenseStatus.PAID}'}
        response = self.client.post(url, data)
        if response.status_code != status.HTTP_201_CREATED:
            print("POST response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 3)


    def test_expense_retrieve_update_delete_view(self):
        # Test GET request
        url = reverse('expense-detail', args=[self.expense1.id]) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], 'Food')

        # Test PUT request
        data = {'category': 'Updated Food', 'amount': 120.00, 'due_date': '2025-01-04', 'notes': 'Dinner'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.status_code != status.HTTP_200_OK:
            print("PUT response data:", response.data)
        self.expense1.refresh_from_db()
        self.assertEqual(self.expense1.category, 'Updated Food')

        # Test DELETE request
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Expense.objects.count(), 1)