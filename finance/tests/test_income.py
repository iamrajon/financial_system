# tests/test_income_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from finance.models import Income
from accounts.models import User

class IncomeViewsTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(email="test.user@example.com", username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(email="test.user@example.com", password='testpass')

        # Create some test income data
        self.income1 = Income.objects.create(user=self.user, source_name='Job', amount=1000, date_received='2023-01-01', status=Income.IncomeStatus.RECEIVED)
        self.income2 = Income.objects.create(user=self.user, source_name='Freelance', amount=500, date_received='2023-02-01', status=Income.IncomeStatus.RECEIVED)

    def test_income_list_create_view(self):
        # Test GET request
        url = reverse('income-list-create')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # Test POST request
        data = {'source_name': 'Gift', 'amount': 200, 'date_received': '2023-03-01', status: f'{Income.IncomeStatus.RECEIVED}'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 3)


    def test_income_retrieve_update_delete_view(self):
        # Test GET request
        url = reverse('income-detail', args=[self.income1.id])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['source_name'], 'Job')
        self.assertEqual(response.data['amount'], '1000.00')
        self.assertEqual(response.data['date_received'], '2023-01-01')
        self.assertEqual(response.data['status'], f'{Income.IncomeStatus.RECEIVED}')

        # Test PUT request
        data = {'source_name': 'Updated Job', 'amount': 1200, 'date_received': '2023-01-01'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.income1.refresh_from_db()
        self.assertEqual(self.income1.source_name, 'Updated Job')

        # Test DELETE request
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Income.objects.count(), 1)