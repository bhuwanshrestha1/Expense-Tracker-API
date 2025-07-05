from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import ExpenseIncome
from decimal import Decimal

class AuthTests(APITestCase):
    def test_user_registration(self):
        """Ensure we can register a new user."""
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword123'}
        response = self.client.post('/api/auth/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        """Ensure a registered user can log in and get tokens."""
        User.objects.create_user(username='testuser', password='testpassword123')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post('/api/auth/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

class ExpenseIncomeAPITests(APITestCase):
    def setUp(self):
        # Create a regular user and a superuser
        self.user = User.objects.create_user(username='user1', password='password123')
        self.superuser = User.objects.create_superuser(username='admin', password='password123')
        
        # Create a record for the regular user
        self.record1 = ExpenseIncome.objects.create(
            user=self.user, title='Groceries', amount=Decimal('100.00'), transaction_type='debit'
        )

    def test_create_record(self):
        """Ensure authenticated user can create a record."""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Salary', 'amount': '5000.00', 'transaction_type': 'credit'}
        response = self.client.post('/api/expenses/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpenseIncome.objects.count(), 2)

    def test_list_own_records(self):
        """Ensure user can only list their own records."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Groceries')

    def test_regular_user_cannot_see_others_records(self):
        """Ensure regular user cannot see records of other users."""
        other_user = User.objects.create_user(username='user2', password='password123')
        ExpenseIncome.objects.create(user=other_user, title='Other User Expense', amount=50, transaction_type='debit')
        
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/expenses/')
        self.assertEqual(len(response.data['results']), 1) # Should only see their own record

    def test_superuser_can_see_all_records(self):
        """Ensure superuser can see all records."""
        other_user = User.objects.create_user(username='user2', password='password123')
        ExpenseIncome.objects.create(user=other_user, title='Other User Expense', amount=50, transaction_type='debit')

        self.client.force_authenticate(user=self.superuser)
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_flat_tax_calculation(self):
        """Test total calculation with flat tax."""
        self.client.force_authenticate(user=self.user)
        record = ExpenseIncome.objects.create(
            user=self.user, title='Consulting Fee', amount=Decimal('1000.00'), 
            transaction_type='credit', tax=Decimal('50.00'), tax_type='flat'
        )
        response = self.client.get(f'/api/expenses/{record.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total']), Decimal('1050.00'))

    def test_percentage_tax_calculation(self):
        """Test total calculation with percentage tax."""
        self.client.force_authenticate(user=self.user)
        record = ExpenseIncome.objects.create(
            user=self.user, title='Software Sale', amount=Decimal('200.00'), 
            transaction_type='credit', tax=Decimal('10.00'), tax_type='percentage' # 10% tax
        )
        response = self.client.get(f'/api/expenses/{record.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data['total']), Decimal('220.00')) # 200 + (200 * 10/100)