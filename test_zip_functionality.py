#!/usr/bin/env python3
"""
Test script to verify zip functionality works correctly
"""

import zipfile
import io

def test_zip_creation():
    """Test creating a zip file with sample documents"""
    print("Testing ZIP creation functionality...")
    
    # Sample HTML content
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Document</title>
    </head>
    <body>
        <h1>Test Document</h1>
        <p>This is a test document for ZIP functionality.</p>
    </body>
    </html>
    """
    
    # Sample PDF content (just dummy bytes for testing)
    pdf_content = b"%PDF-1.4\n%Test PDF content for ZIP functionality"
    
    # Create in-memory zip file
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add HTML file to zip
        zip_file.writestr("test_document.html", html_content)
        
        # Add PDF file to zip
        zip_file.writestr("test_document.pdf", pdf_content)
    
    zip_buffer.seek(0)
    
    # Verify the zip file can be read
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        file_list = zip_file.namelist()
        print(f"Files in ZIP: {file_list}")
        
        # Read content back
        html_data = zip_file.read("test_document.html")
        pdf_data = zip_file.read("test_document.pdf")
        
        print(f"HTML content length: {len(html_data)} bytes")
        print(f"PDF content length: {len(pdf_data)} bytes")
    
    print("✅ ZIP creation test passed!")
    return zip_buffer

if __name__ == "__main__":
    test_zip_creation()