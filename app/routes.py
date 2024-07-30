from flask import Blueprint, request, jsonify
from .database import db
from .models import User, Expense, Split
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Daily Expense Sharing App!"})

@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    email = data['email']
    name = data['name']
    mobile = data['mobile']

    user = User(email=email, name=name, mobile=mobile)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully!"}), 201

@bp.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'mobile': user.mobile
    })

@bp.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    description = data['description']
    total_amount = data['total_amount']
    split_method = data['split_method']
    date = datetime.strptime(data['date'], '%Y-%m-%d')
    user_id = data['user_id']
    splits = data['splits']

    expense = Expense(description=description, total_amount=total_amount, split_method=split_method, date=date, user_id=user_id)
    db.session.add(expense)
    db.session.commit()

    for split in splits:
        split_record = Split(amount=split['amount'], user_id=split['user_id'], expense_id=expense.id)
        db.session.add(split_record)

    db.session.commit()

    return jsonify({"message": "Expense added successfully!"}), 201

@bp.route('/expense/<int:user_id>', methods=['GET'])
def get_user_expenses(user_id):
    expenses = Expense.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': expense.id,
        'description': expense.description,
        'total_amount': expense.total_amount,
        'split_method': expense.split_method,
        'date': expense.date.strftime('%Y-%m-%d'),
        'user_id': expense.user_id
    } for expense in expenses])

@bp.route('/balance-sheet', methods=['GET'])
def get_balance_sheet():
    users = User.query.all()
    balance_sheet = {}
    for user in users:
        total_expenses = db.session.query(db.func.sum(Expense.total_amount)).filter_by(user_id=user.id).scalar() or 0
        owed_amount = db.session.query(db.func.sum(Split.amount)).filter_by(user_id=user.id).scalar() or 0
        balance_sheet[user.id] = {
            'name': user.name,
            'total_expenses': total_expenses,
            'owed_amount': owed_amount
        }
    return jsonify(balance_sheet)
