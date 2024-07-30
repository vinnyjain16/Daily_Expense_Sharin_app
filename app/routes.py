from flask import Blueprint, request
from flask_restful import Api, Resource
from .models import User, Expense, Split
from .database import db

bp = Blueprint('api', __name__)
api = Api(bp)

class UserResource(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(email=data['email'], name=data['name'], mobile=data['mobile'])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return {"id": user.id, "email": user.email, "name": user.name, "mobile": user.mobile}

class ExpenseResource(Resource):
    def post(self):
        data = request.get_json()
        user_id = data['user_id']
        description = data['description']
        total_amount = data['total_amount']
        split_method = data['split_method']
        splits = data['splits']
        
        new_expense = Expense(user_id=user_id, description=description, total_amount=total_amount, split_method=split_method)
        db.session.add(new_expense)
        db.session.commit()
        
        for split in splits:
            new_split = Split(expense_id=new_expense.id, user_id=split['user_id'], amount=split['amount'])
            db.session.add(new_split)
        
        db.session.commit()
        return {"message": "Expense added successfully"}, 201
    
    def get(self, user_id):
        expenses = Expense.query.filter_by(user_id=user_id).all()
        return [{"id": e.id, "description": e.description, "total_amount": e.total_amount, "split_method": e.split_method} for e in expenses]

class BalanceSheetResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        expenses = Expense.query.filter_by(user_id=user_id).all()
        balance_sheet = {
            "user": {"email": user.email, "name": user.name, "mobile": user.mobile},
            "expenses": [{"description": e.description, "total_amount": e.total_amount, "split_method": e.split_method} for e in expenses]
        }
        return balance_sheet

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(ExpenseResource, '/expenses', '/expenses/<int:user_id>')
api.add_resource(BalanceSheetResource, '/balance-sheet/<int:user_id>')
