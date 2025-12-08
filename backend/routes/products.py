"""
Product Routes for BillGenerator Flask Backend
Performance improvements: Pagination and input validation
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from pydantic import BaseModel, Field, ValidationError
from typing import Optional
from ..models.product import Product, db

bp = Blueprint('products', __name__, url_prefix='/api/products')

# Pydantic models for input validation - Code Quality improvement
class ProductCreate(BaseModel):
    """Model for creating a product"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0)

class ProductUpdate(BaseModel):
    """Model for updating a product"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)

@bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products with pagination - Performance improvement"""
    try:
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 10
            
        # Paginate results
        products_paginated = Product.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dict and return with pagination metadata
        return jsonify({
            'products': [product.to_dict() for product in products_paginated.items],
            'pagination': {
                'total': products_paginated.total,
                'pages': products_paginated.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': products_paginated.has_next,
                'has_prev': products_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get products: {str(e)}'}), 500

@bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    """Get a specific product"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
            
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get product: {str(e)}'}), 500

@bp.route('', methods=['POST'])
@jwt_required()
def create_product():
    """Create a new product with input validation - Code Quality improvement"""
    try:
        # Validate input using Pydantic - Code Quality improvement
        try:
            product_data = ProductCreate(**request.get_json())
        except ValidationError as e:
            return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400
        
        # Create new product
        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price
        )
        
        # Save to database
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'product': product.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create product: {str(e)}'}), 500

@bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update an existing product with input validation - Code Quality improvement"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Validate input using Pydantic - Code Quality improvement
        try:
            product_data = ProductUpdate(**request.get_json())
        except ValidationError as e:
            return jsonify({'error': 'Validation failed', 'details': e.errors()}), 400
        
        # Update fields if provided
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.price is not None:
            product.price = product_data.price
        
        # Save changes
        db.session.commit()
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update product: {str(e)}'}), 500

@bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete a product"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
            
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete product: {str(e)}'}), 500