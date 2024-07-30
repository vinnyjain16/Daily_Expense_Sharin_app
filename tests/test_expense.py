import unittest
from app import create_app
from app.database import db
from app.models import User, Expense, Split

class ExpenseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.client.post('/api/users', json={
            'email': 'user1@example.com',
            'name': 'User One',
            'mobile': '1234567890'
        })
        self.client.post('/api/users', json={
            'email': 'user2@example.com',
            'name': 'User Two',
            'mobile': '0987654321'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_expense(self):
        response = self.client.post('/api/expenses', json={
            'user_id': 1,
            'description': 'Groceries',
            'total_amount': 500,
            'split_method': 'equal',
            'splits': [
                {'user_id': 1, 'amount': 250},
                {'user_id': 2, 'amount': 250}
            ]
        })
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
