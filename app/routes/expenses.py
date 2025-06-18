from flask import Blueprint, request, jsonify
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models import User, Expense
from sqlalchemy import func

expenses_bp = Blueprint('expenses',__name__,url_prefix='/expenses')

@expenses_bp.route('/',methods=['GET'])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=current_user)\
        .order_by(Expense.date.desc())\
            .all()
    result = []
    for ex in expenses:
        result.append({
            'id': ex.id,
            'amount': ex.amount,
            'category': ex.category,
            'description':ex.description,
            'date':ex.date
            })
    return jsonify(result),200
@expenses_bp.route('/',methods=['POST'])
@jwt_required()
def add_expense():
    current_user = get_jwt_identity()
    data = request.get_json()

    amount = data.get('amount')
    category = data.get('category')
    description = data.get('description')

    if not amount or not isinstance(amount,(int,float))or amount<=0:
        return jsonify({'message':'amount msut be a positive number'}),400
    if not category:
        return jsonify({'message':'please enter category'}),400
    if len(category) > 100:
        return jsonify({'message':'category is too long'}),400
    if description and len(description) > 200:
        return jsonify({'message':'Description is too long'}),400
                       
    
    new_expense = Expense(
        amount=amount,
        category=category,
        description=description,
        user_id=current_user)

    try:
        db.session.add(new_expense)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message':'error adding expense'}),500
    
    return jsonify({
        'message':'Expense added',
        'expense':{
            'id': new_expense.id,
            'amount': new_expense.amount,
            'category': new_expense.category,
            'description': new_expense.description,
            'date': new_expense.date.strftime('%Y-%m-%d %H:%M:%S')
        }}),201
@expenses_bp.route('/by-category',methods=['GET'])
@jwt_required()
def get_expenses_by_category():
    current_user = get_jwt_identity()

    category_totals =db.session.query(
        Expense.category,
        func.sum(Expense.amount).label('total_amount'),
        func.count(Expense.id).label('count')
    ).filter(
        Expense.user_id == current_user
    ).group_by(
        Expense.category
    ).all()

    result = []
    for category, total_amount, count in category_totals:
        result.append({
            'category': category,
            'total_amount': float(total_amount),
            'count': count
        })
    return jsonify(result)

@expenses_bp.route('/<int:id>',methods=['PUT'])
@jwt_required()
def update_expense(id):
    current_user = get_jwt_identity()
    data = request.get_json()
    expense = Expense.query.filter_by(id = id, user_id=current_user).first()
    
    if not expense:
        return jsonify({'message':'expense not found'}),404
    
    if 'amount' in data:
        if not isinstance(data['amount'], (int,float)) or data['amount'] <=0:
          return jsonify({'message':'amount must be a positive number'}),400
        expense.amount = data['amount']
    
    if 'category' in data:
        if not data['category'] or len(data['category']) > 100:
            return jsonify({'message':'invalid category'}),400
        expense.category = data['category']
    
    if 'description' in data:
        if not data['description'] or len(data['description']) > 200:
            return jsonify({'message':'description is too long'}),400
        expense.description = data['description']
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message':'error updatind expense'}),400
    
    return jsonify({
       'id': expense.id,
       'amount': expense.amount,
       'category':expense.category,
       'description':expense.description,
       'date': expense.date
    }),201

@expenses_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_expense(id):
    current_user = get_jwt_identity()
    expense = Expense.query.filter_by(id = id, user_id = current_user).first()

    if not expense:
        return jsonify ({'message':'invalid expense'}),404
    return jsonify({
         'id': expense.id,
            'amount': expense.amount,
            'category': expense.category,
            'description':expense.description,
            'date':expense.date}),201

@expenses_bp.route('/<int:id>',methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    pass