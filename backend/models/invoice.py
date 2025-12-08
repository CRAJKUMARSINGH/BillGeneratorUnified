"""
Invoice Model for BillGenerator Flask Backend
"""
from backend.db import db
from datetime import datetime

class Invoice(db.Model):
    """Invoice model"""
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    work_order_number = db.Column(db.String(50), nullable=False)
    bill_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    amount_paid = db.Column(db.Float, default=0.0)
    unpaid_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('invoices', lazy=True))
    
    def to_dict(self):
        """Convert invoice object to dictionary"""
        return {
            'id': self.id,
            'invoice_number': self.invoice_number,
            'client_name': self.client_name,
            'work_order_number': self.work_order_number,
            'bill_date': self.bill_date.isoformat() if self.bill_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'subtotal': self.subtotal,
            'total_amount': self.total_amount,
            'amount_paid': self.amount_paid,
            'unpaid_amount': self.unpaid_amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'