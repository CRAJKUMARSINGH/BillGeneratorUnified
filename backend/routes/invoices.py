"""
Invoice Routes for BillGenerator Flask Backend
Performance improvements: Joined loading and pagination
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload
from ..models.invoice import Invoice, db
from ..models.user import User

bp = Blueprint('invoices', __name__, url_prefix='/api/invoices')

@bp.route('', methods=['GET'])
@jwt_required()
def get_invoices():
    """Get all invoices with pagination and optimized queries - Performance improvement"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        # Query invoices with joined loading to prevent N+1 problem - Performance improvement
        invoices_query = Invoice.query.options(
            joinedload(Invoice.user)  # Eager load user data
        ).order_by(Invoice.created_at.desc())
        
        # Paginate results
        invoices_paginated = invoices_query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dict and return with pagination metadata
        return jsonify({
            'invoices': [invoice.to_dict() for invoice in invoices_paginated.items],
            'pagination': {
                'total': invoices_paginated.total,
                'pages': invoices_paginated.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': invoices_paginated.has_next,
                'has_prev': invoices_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get invoices: {str(e)}'}), 500

@bp.route('/<int:invoice_id>', methods=['GET'])
@jwt_required()
def get_invoice(invoice_id):
    """Get a specific invoice with optimized query"""
    try:
        # Use joined loading to prevent N+1 problem - Performance improvement
        invoice = Invoice.query.options(
            joinedload(Invoice.user)  # Eager load user data
        ).get(invoice_id)
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
            
        return jsonify({'invoice': invoice.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get invoice: {str(e)}'}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_invoice():
    """Create a new invoice"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['invoice_number', 'client_name', 'work_order_number', 
                          'bill_date', 'due_date', 'subtotal', 'total_amount']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create new invoice
        invoice = Invoice(
            invoice_number=data['invoice_number'],
            client_name=data['client_name'],
            work_order_number=data['work_order_number'],
            bill_date=data['bill_date'],
            due_date=data['due_date'],
            subtotal=data['subtotal'],
            total_amount=data['total_amount'],
            amount_paid=data.get('amount_paid', 0.0),
            unpaid_amount=data.get('unpaid_amount', data['total_amount']),
            user_id=data.get('user_id')  # Optional, can be set from JWT token
        )
        
        # Save to database
        db.session.add(invoice)
        db.session.commit()
        
        # Return created invoice
        return jsonify({'invoice': invoice.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create invoice: {str(e)}'}), 500

@bp.route('/<int:invoice_id>', methods=['PUT'])
@jwt_required()
def update_invoice(invoice_id):
    """Update an existing invoice"""
    try:
        invoice = Invoice.query.get(invoice_id)
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
            
        data = request.get_json()
        
        # Update fields if provided
        updatable_fields = ['invoice_number', 'client_name', 'work_order_number', 
                           'bill_date', 'due_date', 'subtotal', 'total_amount', 
                           'amount_paid', 'unpaid_amount']
        
        for field in updatable_fields:
            if field in data:
                setattr(invoice, field, data[field])
        
        # Save changes
        db.session.commit()
        
        return jsonify({'invoice': invoice.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update invoice: {str(e)}'}), 500

@bp.route('/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(invoice_id):
    """Delete an invoice"""
    try:
        invoice = Invoice.query.get(invoice_id)
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
            
        db.session.delete(invoice)
        db.session.commit()
        
        return jsonify({'message': 'Invoice deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete invoice: {str(e)}'}), 500