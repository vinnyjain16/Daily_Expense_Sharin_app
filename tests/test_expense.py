# tests/test_expense.py
from tests import BaseTestCase
from app.models import User, Expense, Split

class ExpenseTestCase(BaseTestCase):

    def test_add_expense(self):
        user = User(email='test@example.com', name='Test User', mobile='1234567890')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/expense', json={
            'description': 'Dinner',
            'total_amount': 3000,
            'split_method': 'equal',
            'date': '2023-07-28',
            'user_id': user.id,
            'splits': [
                {'amount': 1500, 'user_id': user.id},
                {'amount': 1500, 'user_id': user.id}
            ]
        })
        self.assertEqual(response.status_code, 201)

    # Add more test methods as needed

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_expense(self):
        response = self.client.post('/expense', json={
            'description': 'Dinner',
            'total_amount': 3000,
            'split_method': 'equal',
            'date': '2023-07-28',
            'user_id': self.user1.id,
            'splits': [
                {'amount': 1500, 'user_id': self.user1.id},
                {'amount': 1500, 'user_id': self.user2.id}
            ]
        })
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
