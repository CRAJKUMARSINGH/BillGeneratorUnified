"""
Test cases for the invoices API endpoints.
"""
import pytest
import json
from datetime import date
from backend.models.user import db, User
from backend.models.invoice import Invoice

def test_get_invoices_empty(client, auth_header):
    """Test getting invoices when none exist."""
    response = client.get('/api/invoices', headers=auth_header)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'invoices' in data
    assert 'pagination' in data
    assert len(data['invoices']) == 0

def test_create_invoice(client, auth_header):
    """Test creating a new invoice."""
    invoice_data = {
        'invoice_number': 'INV-TEST-001',
        'client_name': 'Test Client',
        'work_order_number': 'WO-TEST-001',
        'bill_date': '2023-01-15',
        'due_date': '2023-02-15',
        'subtotal': 1000.0,
        'total_amount': 1180.0
    }
    
    response = client.post('/api/invoices', 
                          data=json.dumps(invoice_data),
                          headers={**auth_header, 'Content-Type': 'application/json'})
    
    assert response.status_code == 201
    
    data = json.loads(response.data)
    assert 'invoice' in data
    assert data['invoice']['invoice_number'] == 'INV-TEST-001'
    assert data['invoice']['client_name'] == 'Test Client'

def test_get_invoices_pagination(client, auth_header):
    """Test getting invoices with pagination."""
    response = client.get('/api/invoices?page=1&per_page=1', headers=auth_header)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'invoices' in data
    assert 'pagination' in data
    assert len(data['invoices']) <= 1
    assert data['pagination']['per_page'] == 1

def test_get_specific_invoice(client, auth_header):
    """Test getting a specific invoice."""
    # First create an invoice
    invoice_data = {
        'invoice_number': 'INV-TEST-002',
        'client_name': 'Test Client 2',
        'work_order_number': 'WO-TEST-002',
        'bill_date': '2023-01-16',
        'due_date': '2023-02-16',
        'subtotal': 2000.0,
        'total_amount': 2360.0
    }
    
    client.post('/api/invoices', 
                data=json.dumps(invoice_data),
                headers={**auth_header, 'Content-Type': 'application/json'})
    
    # Get the first invoice
    response = client.get('/api/invoices/1', headers=auth_header)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'invoice' in data
    assert data['invoice']['id'] == 1

def test_get_nonexistent_invoice(client, auth_header):
    """Test getting a nonexistent invoice."""
    response = client.get('/api/invoices/99999', headers=auth_header)
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data

def test_update_invoice(client, auth_header):
    """Test updating an existing invoice."""
    # First create an invoice
    invoice_data = {
        'invoice_number': 'INV-TEST-003',
        'client_name': 'Test Client 3',
        'work_order_number': 'WO-TEST-003',
        'bill_date': '2023-01-17',
        'due_date': '2023-02-17',
        'subtotal': 3000.0,
        'total_amount': 3540.0
    }
    
    client.post('/api/invoices', 
                data=json.dumps(invoice_data),
                headers={**auth_header, 'Content-Type': 'application/json'})
    
    update_data = {
        'client_name': 'Updated Client Name',
        'total_amount': 1500.0
    }
    
    response = client.put('/api/invoices/1',
                         data=json.dumps(update_data),
                         headers={**auth_header, 'Content-Type': 'application/json'})
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'invoice' in data
    assert data['invoice']['client_name'] == 'Updated Client Name'
    assert data['invoice']['total_amount'] == 1500.0

def test_delete_invoice(client, auth_header):
    """Test deleting an invoice."""
    # First create an invoice
    invoice_data = {
        'invoice_number': 'INV-TEST-004',
        'client_name': 'Test Client 4',
        'work_order_number': 'WO-TEST-004',
        'bill_date': '2023-01-18',
        'due_date': '2023-02-18',
        'subtotal': 4000.0,
        'total_amount': 4720.0
    }
    
    client.post('/api/invoices', 
                data=json.dumps(invoice_data),
                headers={**auth_header, 'Content-Type': 'application/json'})
    
    # First, check that the invoice exists
    response = client.get('/api/invoices/1', headers=auth_header)
    assert response.status_code == 200
    
    # Delete the invoice
    response = client.delete('/api/invoices/1', headers=auth_header)
    assert response.status_code == 200
    
    # Verify it's deleted
    response = client.get('/api/invoices/1', headers=auth_header)
    assert response.status_code == 404