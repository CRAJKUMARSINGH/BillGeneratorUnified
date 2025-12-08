"""
Test script for refactored document generators
"""

def test_imports():
    """Test that all generator classes can be imported"""
    try:
        from core.generators.base_generator import BaseGenerator
        print("✓ BaseGenerator import successful")
    except Exception as e:
        print(f"✗ BaseGenerator import failed: {e}")
    
    try:
        from core.generators.html_generator import HTMLGenerator
        print("✓ HTMLGenerator import successful")
    except Exception as e:
        print(f"✗ HTMLGenerator import failed: {e}")
    
    try:
        from core.generators.pdf_generator import PDFGenerator
        print("✓ PDFGenerator import successful")
    except Exception as e:
        print(f"✗ PDFGenerator import failed: {e}")
    
    try:
        from core.generators.doc_generator import DOCGenerator
        print("✓ DOCGenerator import successful")
    except Exception as e:
        print(f"✗ DOCGenerator import failed: {e}")
    
    try:
        from core.generators.template_manager import TemplateManager
        print("✓ TemplateManager import successful")
    except Exception as e:
        print(f"✗ TemplateManager import failed: {e}")
    
    try:
        from core.generators.document_generator import DocumentGenerator
        print("✓ DocumentGenerator import successful")
    except Exception as e:
        print(f"✗ DocumentGenerator import failed: {e}")
    
    try:
        from core.generators import BaseGenerator, HTMLGenerator, PDFGenerator, DOCGenerator, TemplateManager, DocumentGenerator
        print("✓ Package import successful")
    except Exception as e:
        print(f"✗ Package import failed: {e}")

def test_class_instantiation():
    """Test that generator classes can be instantiated"""
    # Mock data for testing
    mock_data = {
        'title_data': {},
        'work_order_data': None,
        'bill_quantity_data': None,
        'extra_items_data': None,
    }
    
    try:
        from core.generators.base_generator import BaseGenerator
        base_gen = BaseGenerator(mock_data)
        print("✓ BaseGenerator instantiation successful")
    except Exception as e:
        print(f"✗ BaseGenerator instantiation failed: {e}")
    
    try:
        from core.generators.html_generator import HTMLGenerator
        html_gen = HTMLGenerator(mock_data)
        print("✓ HTMLGenerator instantiation successful")
    except Exception as e:
        print(f"✗ HTMLGenerator instantiation failed: {e}")
    
    try:
        from core.generators.pdf_generator import PDFGenerator
        pdf_gen = PDFGenerator(mock_data)
        print("✓ PDFGenerator instantiation successful")
    except Exception as e:
        print(f"✗ PDFGenerator instantiation failed: {e}")
    
    try:
        from core.generators.doc_generator import DOCGenerator
        doc_gen = DOCGenerator(mock_data)
        print("✓ DOCGenerator instantiation successful")
    except Exception as e:
        print(f"✗ DOCGenerator instantiation failed: {e}")
    
    try:
        from core.generators.template_manager import TemplateManager
        template_mgr = TemplateManager()
        print("✓ TemplateManager instantiation successful")
    except Exception as e:
        print(f"✗ TemplateManager instantiation failed: {e}")
    
    try:
        from core.generators.document_generator import DocumentGenerator
        doc_gen = DocumentGenerator(mock_data)
        print("✓ DocumentGenerator instantiation successful")
    except Exception as e:
        print(f"✗ DocumentGenerator instantiation failed: {e}")

if __name__ == "__main__":
    print("Testing refactored document generators...")
    print("\n1. Testing imports:")
    test_imports()
    
    print("\n2. Testing class instantiation:")
    test_class_instantiation()
    
    print("\nRefactored generator testing complete!")