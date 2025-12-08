"""
User Routes for BillGenerator Flask Backend
Performance improvements: Pagination
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models.user import User, db
from ..utils.cache import cached, cache_manager

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('', methods=['GET'])
@jwt_required()
@cached(expire=300)  # Cache for 5 minutes
def get_users():
    """Get all users with pagination - Performance improvement"""
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
        users_paginated = User.query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Convert to dict and return with pagination metadata
        return jsonify({
            'users': [user.to_dict() for user in users_paginated.items],
            'pagination': {
                'total': users_paginated.total,
                'pages': users_paginated.pages,
                'current_page': page,
                'per_page': per_page,
                'has_next': users_paginated.has_next,
                'has_prev': users_paginated.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get users: {str(e)}'}), 500

@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get a specific user"""
    try:
        # Try to get from cache first
        cache_key = f"user_{user_id}"
        cached_user = cache_manager.get(cache_key)
        if cached_user:
            return jsonify({'user': cached_user}), 200
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # Cache the result
        user_dict = user.to_dict()
        cache_manager.set(cache_key, user_dict, expire=300)  # Cache for 5 minutes
            
        return jsonify({'user': user_dict}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500

@bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update an existing user"""
    try:
        # Try to get from cache first
        cache_key = f"user_{user_id}"
        cached_user = cache_manager.get(cache_key)
        if cached_user:
            cache_manager.delete(cache_key)
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update fields if provided (excluding password for security)
        updatable_fields = ['username', 'email', 'is_active']
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # Handle password update separately
        if 'password' in data:
            user.set_password(data['password'])  # Hash the new password
        
        # Save changes
        db.session.commit()
        
        # Invalidate caches
        cache_manager.delete(f"user_{user_id}")
        cache_manager.flush()  # Invalidate all users cache
        
        # Cache the updated user
        cache_manager.set(f"user_{user.id}", user.to_dict(), expire=300)
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to update user: {str(e)}'}), 500

@bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete a user"""
    try:
        # Try to get from cache first
        cache_key = f"user_{user_id}"
        cached_user = cache_manager.get(cache_key)
        if cached_user:
            cache_manager.delete(cache_key)
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        db.session.delete(user)
        db.session.commit()
        
        # Invalidate caches
        cache_manager.delete(f"user_{user_id}")
        cache_manager.flush()  # Invalidate all users cache
        
        return jsonify({'message': 'User deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500