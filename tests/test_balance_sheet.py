# tests/test_balance_sheet.py
from tests import BaseTestCase
from app.models import User, Expense, Split

class BalanceSheetTestCase(BaseTestCase):

    def test_balance_sheet(self):
        user1 = User(email='user1@example.com', name='User One', mobile='1234567890')
        user2 = User(email='user2@example.com', name='User Two', mobile='0987654321')
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        expense1 = Expense(description='Lunch', total_amount=500, split_method='equal', date='2023-07-28', user_id=user1.id)
        db.session.add(expense1)
        db.session.commit()

        split1 = Split(amount=250, user_id=user1.id, expense_id=expense1.id)
        split2 = Split(amount=250, user_id=user2.id, expense_id=expense1.id)
        db.session.add(split1)
        db.session.add(split2)
        db.session.commit()

        response = self.client.get('/balance-sheet')
        self.assertEqual(response.status_code, 200)

    # Add more test methods as needed
