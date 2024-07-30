import unittest
from app import create_app
from app.database import db
from app.models import User, Expense, Split

class BalanceSheetTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_balance_sheet(self):
        response = self.client.post('/api/users', json={
            'email': 'test@example.com',
            'name': 'Test User',
            'mobile': '1234567890'
        })
        self.assertEqual(response.status_code, 201)
        
        response = self.client.post('/api/expenses', json={
            'user_id': 1,
            'description': 'Dinner',
            'total_amount': 3000,
            'split_method': 'equal',
            'splits': [
                {'user_id': 1, 'amount': 1000},
                {'user_id': 2, 'amount': 1000},
                {'user_id': 3, 'amount': 1000}
            ]
        })
        self.assertEqual(response.status_code, 201)

        response = self.client.get('/api/balance-sheet/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
