"""
Shared database instance for the BillGenerator backend.
"""
from flask_sqlalchemy import SQLAlchemy

# Create a single SQLAlchemy instance to be shared across the application
db = SQLAlchemy()